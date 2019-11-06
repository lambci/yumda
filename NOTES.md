## Running build image for building LambCI repo packages

Assumes access to the `RPM-GPG-KEY-lambci` private key

Amazon Linux 1:

```console
cd amazon-linux-1/build

docker run --rm -it -v $PWD:/tmp/fs lambci/yumda:build-1 bash
gpg --import /tmp/fs/RPM-GPG-KEY-lambci.private
```

Amazon Linux 2:

```console
cd amazon-linux-2/build

docker run --rm -it -v $PWD:/tmp/fs lambci/yumda:build-2 bash
gpg --import /tmp/fs/RPM-GPG-KEY-lambci.private
```

## Checking for remote updates to spec files

Amazon Linux 1:

```console
diff <(ls -1 /tmp/fs/specs/lambda1 | sed 's/.spec$//' | xargs repoquery -s --archlist=x86_64 | sed -e 's/amzn1/lambda1/' -e 's/el6/lambda1/' | sort | uniq) \
  <(ls -1 /tmp/fs/lambda1/SRPMS/Packages | sort) | \
  grep '^<' | \
  grep -v git-2.14.5-1.60.
```

Amazon Linux 2:

```console
diff <(ls -1 /tmp/fs/specs/lambda2 | sed 's/.spec$//' | xargs repoquery -s --archlist=x86_64 | sed -e 's/amzn2/lambda2/' -e 's/el7/lambda2/' | sort | uniq) \
  <(ls -1 /tmp/fs/lambda2/SRPMS/Packages | sort) | \
  grep '^<' | \
  grep -v git-2.17.2-2. | \
  grep -v libvoikko-3.6-5. | \
  grep -v libidn2-2.2.0-1. | \
  grep -v libmetalink-0.1.3-1. | \
  grep -v lzo-2.06-8.
```

## Pulling down Amazon source RPMS

```console
yumdownloader --source gcc # etc...
rpm -ivh *.src.rpm
```

Be aware that clashing deps (eg, `python` and `python3`) can't be unpacked together

## Running diffs on downloaded specs

```console
ls -1 ~/rpmbuild/SPECS

export CURSPEC=ruby.spec # etc...

diff -u /tmp/fs/specs/amzn2/$CURSPEC ~/rpmbuild/SPECS/$CURSPEC

# If needing to copy spec over:
cp ~/rpmbuild/SPECS/$CURSPEC /tmp/fs/specs/amzn2/
cp ~/rpmbuild/SPECS/$CURSPEC /tmp/fs/specs/lambda2/
```

## Adding new specs

```console
cp ~/rpmbuild/SPECS/$CURSPEC /tmp/fs/specs/lambda2/

# Edit as necessary
```

## Building specs

```console
sudo yum-builddep -y /tmp/fs/specs/lambda2/$CURSPEC

rpmbuild -ba --nocheck --sign /tmp/fs/specs/lambda2/$CURSPEC

# If successful...
cp ~/rpmbuild/SPECS/$CURSPEC /tmp/fs/specs/amzn2/
rm ~/rpmbuild/SPECS/$CURSPEC
```

## To bulk sign RPMs

```console
rpm --addsign ~/rpmbuild/{SRPMS,RPMS/*}/*.rpm
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
  aws cloudfront create-invalidation --distribution-id EJS6WO6246GX7 --paths "/lambda1/RPMS/repodata/*" && \
  docker run --rm lambci/yumda:1 yum list available > ../packages.txt
```

Amazon Linux 2:

```console
aws s3 sync --delete ~/github/yumda/amazon-linux-2/build/lambda2 s3://rpm.lambci.org/lambda2 && \
  aws cloudfront create-invalidation --distribution-id EJS6WO6246GX7 --paths "/lambda2/RPMS/repodata/*" && \
  docker run --rm lambci/yumda:2 yum list available > ../packages.txt
```

## Checking that all RPMs install ok

Amazon Linux 1:

```console
docker run --rm lambci/yumda:1 bash -c "yum list available | tail -n +3 | grep -o -E '^\S+' | xargs yum install -y"
```

Amazon Linux 2:

```console
docker run --rm lambci/yumda:2 bash -c "yum list available | tail -n +3 | grep -o -E '^\S+' | grep -v libcrypt-nss | xargs yum install -y"
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
    .filter(t => names.has(t))
"
```

Amazon Linux 2:

```
node -p "
  names = new Set(fs.readFileSync('../packages.txt', 'utf8').trim().split('\n').slice(2)
    .map(p => (p.match(/(^.+)(.x86_64|.noarch)/) || [])[1]).filter(Boolean));
  fs.readFileSync('../todo.amzn2.txt', 'utf8').trim().split('\n')
    .map(t => t.split('.amzn2')[0].split('-').slice(0, -2).join('-'))
    .filter(t => names.has(t))
"
```
