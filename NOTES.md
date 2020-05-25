## Running build image for building LambCI repo packages

Assumes access to the `RPM-GPG-KEY-lambci` private key

Amazon Linux 1:

```console
cd amazon-linux-1/build

docker run --rm -it -v $PWD:/tmp/fs:delegated lambci/yumda:build-1 bash
gpg --import /tmp/fs/RPM-GPG-KEY-lambci.private
```

Amazon Linux 2:

```console
cd amazon-linux-2/build

docker run --rm -it -v $PWD:/tmp/fs:delegated lambci/yumda:build-2 bash
gpg --import /tmp/fs/RPM-GPG-KEY-lambci.private
```

## Checking for remote updates to spec files

Amazon Linux 1:

```console
docker run --rm -v $PWD:/tmp/fs lambci/yumda:build-1 bash -c "
  diff <(ls -1 /tmp/fs/specs/lambda1 | sed 's/.spec$//' | xargs repoquery -s --archlist=x86_64,noarch | \
    grep -v -e git-2.14 -e libwebp-0.4.3-3.el6 | \
    sed -e 's/amzn1/lambda1/' -e 's/el6/lambda1/' | sort | uniq) \
    <(ls -1 /tmp/fs/lambda1/SRPMS/Packages | sort) | \
    grep '^<'"
```

Amazon Linux 2:

```console
docker run --rm -v $PWD:/tmp/fs lambci/yumda:build-2 bash -c "
  diff <(ls -1 /tmp/fs/specs/lambda2 | sed 's/.spec$//' | xargs repoquery -s --archlist=x86_64,noarch | \
    grep -v -e git-2.23.3-1.amzn2 -e libvoikko-3.6-5.amzn2 -e lzo-2.06-8.amzn2 \
      -e libidn2-2.3.0-1.el7 -e libmetalink-0.1.3-1.el7 -e pngquant-2.7.2-3.el7 | \
    sed -e 's/amzn2/lambda2/' -e 's/el7/lambda2/' | sort | uniq) \
    <(ls -1 /tmp/fs/lambda2/SRPMS/Packages | sort) | \
    grep '^<'"
```

## Pulling down Amazon source RPMS

```console
yumdownloader --source gcc # etc...
rpm -ivh *.src.rpm
```

Be aware that clashing deps (eg, `python` and `python3`) can't be unpacked together

## Patching lambda specs from amzn diffs

From outside docker, assuming amzn updates have been committed

Amazon Linux 1:

```console
for CURSPEC in openssh; do
  git diff origin/master -- specs/amzn1/${CURSPEC}.spec | patch specs/lambda1/${CURSPEC}.spec;
done
```

Amazon Linux 2:

```console
for CURSPEC in openssh; do
  git diff origin/master -- specs/amzn2/${CURSPEC}.spec | patch specs/lambda2/${CURSPEC}.spec;
done
```

## Building specs

Amazon Linux 1:

```console
export CURSPEC=openssh && \
  rm -rf ~/rpmbuild/{S,}RPMS && \
  sudo yum-builddep -y /tmp/fs/specs/lambda1/${CURSPEC}.spec && \
  rpmbuild -ba --nocheck --sign /tmp/fs/specs/lambda1/${CURSPEC}.spec
```

Amazon Linux 2:

```console
export CURSPEC=openssh && \
  rm -rf ~/rpmbuild/{S,}RPMS && \
  sudo yum-builddep -y /tmp/fs/specs/lambda2/${CURSPEC}.spec && \
  rpmbuild -ba --nocheck --sign /tmp/fs/specs/lambda2/${CURSPEC}.spec
```

## To bulk sign RPMs

```console
rpm --addsign ~/rpmbuild/{SRPMS,RPMS/*}/*.rpm
```

## Manually installing RPMs

Downloading:
```console
yumdownloader --destdir /tmp/fs java-1.8.0-openjdk-devel
```

Installing:
```console
yum localinstall -y /app/java-1.8.0-openjdk-devel-*.rpm
```

Installing with a different prefix:
```console
rpm -ivh --root=/lambda --prefix=/tmp /app/java-1.8.0-openjdk-devel-*.rpm
```

## Copying over RPMs and updating yum repo

Amazon Linux 1:

```console
cp ~/rpmbuild/RPMS/*/*.rpm /tmp/fs/lambda1/RPMS/Packages/ && \
  cp ~/rpmbuild/SRPMS/*.rpm /tmp/fs/lambda1/SRPMS/Packages/ && \
  for dir in RPMS SRPMS; do createrepo --update /tmp/fs/lambda1/$dir; done
```

Amazon Linux 2:

```console
cp ~/rpmbuild/RPMS/*/*.rpm /tmp/fs/lambda2/RPMS/Packages/ && \
  cp ~/rpmbuild/SRPMS/*.rpm /tmp/fs/lambda2/SRPMS/Packages/ && \
  for dir in RPMS SRPMS; do createrepo --update /tmp/fs/lambda2/$dir; done
```

## Syncing to S3

Amazon Linux 1:

```console
aws s3 sync --delete ~/github/yumda/amazon-linux-1/build/lambda1 s3://rpm.lambci.org/lambda1 && \
  aws cloudfront create-invalidation --distribution-id EJS6WO6246GX7 --paths "/lambda1/RPMS/*" && \
  docker run --rm lambci/yumda:1 yum list available > ../packages.txt
```

Amazon Linux 2:

```console
aws s3 sync --delete ~/github/yumda/amazon-linux-2/build/lambda2 s3://rpm.lambci.org/lambda2 && \
  aws cloudfront create-invalidation --distribution-id EJS6WO6246GX7 --paths "/lambda2/RPMS/*" && \
  docker run --rm lambci/yumda:2 yum list available > ../packages.txt
```

## Checking that all RPMs install ok

Amazon Linux 1:

```console
docker run --rm lambci/yumda:1 bash -c "
  yum list available | tail -n +3 | grep -o -E '^\S+' | xargs yum install"
```

Amazon Linux 2:

```console
docker run --rm lambci/yumda:2 bash -c "
  yum list available | tail -n +3 | grep -o -E '^\S+' | grep -v -e libcrypt-nss -e llvm-private | xargs yum install"
```

Checking for hardlinks from lambci/yumda:
```console
chroot /lambda find /opt -type f -links +1 -printf '%i %n %p\n' | sort -n
```

Checking for broken symlinks from lambci/yumda:
```console
chroot /lambda find /opt -xtype l -printf '%p -> %l\n' | grep -v -e '-> /usr'
```

Checking for absolute symlinks from lambci/yumda:
```console
chroot /lambda find /opt -type l -lname '/*' -printf '%p -> %l\n' | grep -v -e '-> /usr' -e '-> /lib64'
```

## Generating todo.txt

```
for pkg in $(repoquery -a --archlist=x86_64,noarch --nvr); do
  echo $pkg $(repoquery -q --whatrequires --archlist=x86_64,noarch --nvr $pkg | awk -F- '{for (i=1; i<NF-1; i++) printf("%s-",$i); printf("\n")}' | sort | uniq | wc -l)
done
```

## Comparing generated RPMs with originals

```
diff <(rpm -qpl compat-gcc-48-4.8.5-16.amzn2.0.2.x86_64.rpm | sed 's|^/usr/|/opt/|' | sort) \
  <(rpm -qpl /tmp/fs/lambda2/RPMS/Packages/compat-gcc-48-4.8.5-16.lambda2.0.2.x86_64.rpm | sort)
```

## Which packages should be removed from the TODO lists

Amazon Linux 1:

```
node -p "
  names = new Set(fs.readFileSync('../packages.txt', 'utf8').trim().split('\n').slice(2)
    .map(p => (p.match(/(^.+)(.x86_64|.noarch)/) || [])[1]).filter(Boolean));
  fs.readFileSync('../todo.amzn1.txt', 'utf8').trim().split('\n')
    .map(t => t.split('.amzn1')[0].split('-').slice(0, -2).join('-'))
    .filter(t => names.has(t))"
```

Amazon Linux 2:

```
node -p "
  names = new Set(fs.readFileSync('../packages.txt', 'utf8').trim().split('\n').slice(2)
    .map(p => (p.match(/(^.+)(.x86_64|.noarch)/) || [])[1]).filter(Boolean));
  fs.readFileSync('../todo.amzn2.txt', 'utf8').trim().split('\n')
    .map(t => t.split('.amzn2')[0].split('-').slice(0, -2).join('-'))
    .filter(t => names.has(t))"
```

## Querying metadata on existing RPM file

rpm -qp --qf "\
[Name: %{NAME}\n]\
[Version: %{VERSION}\n]\
[Release: %{RELEASE}\n]\
[Epoch: %{EPOCH}\n]\
[Summary: %{SUMMARY}\n]\
[Group: %{GROUP}\n]\
[License: %{LICENSE}\n]\
[Url: %{URL}\n]\
[Conflicts: %{CONFLICTS}\n]\
[Obsoletes: %{OBSOLETES}\n]\
[Provides: %{PROVIDES}\n]\
[Recommends: %{RECOMMENDS}\n]\
[Requires: %{REQUIRES}\n]\
[description: %{DESCRIPTION}\n]\
[prein: %{PREIN}\n]\
[preun: %{PREUN}\n]\
[pretrans: %{PRETRANS}\n]\
[postin: %{POSTIN}\n]\
[postun: %{POSTUN}\n]\
[posttrans: %{POSTTRANS}\n]\
" \
*.rpm
