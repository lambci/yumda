## Running build image for building LambCI repo packages

Assumes access to the `RPM-GPG-KEY-lambci` private key

```console
cd amazon-linux-2/build

docker run --rm -it -v $PWD:/tmp/fs lambci/yumda:build-2 bash
gpg --import /tmp/fs/RPM-GPG-KEY-lambci.private
```

## Checking for remote updates to spec files

```console
diff <(ls -1 /tmp/fs/specs/lambda2 | sed 's/.spec$//' | xargs repoquery -s | sed -e 's/amzn2/lambda2/' -e 's/el7/lambda2/' | sort | uniq) \
  <(ls -1 /tmp/fs/lambda2/SRPMS/Packages | sort) | \
  grep '^<' | \
  grep -v git-2.17.2-2.lambda2.src.rpm | \
  grep -v libvoikko-3.6-5.lambda2.0.1.src.rpm
```

## Pulling down Amazon source RPMS

```console
yumdownloader --source gcc # etc...
sudo yum-builddep -y *.src.rpm
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

```console
cp ~/rpmbuild/RPMS/*/*.rpm /tmp/fs/lambda2/RPMS/Packages/
cp ~/rpmbuild/SRPMS/*.rpm /tmp/fs/lambda2/SRPMS/Packages/
for dir in RPMS SRPMS; do createrepo --update /tmp/fs/lambda2/$dir; done
```

## Syncing to S3

```console
aws s3 sync --delete ~/github/yumda/amazon-linux-2/build/lambda2 s3://rpm.lambci.org/lambda2 && \
  aws cloudfront create-invalidation --distribution-id EJS6WO6246GX7 --paths "/lambda2/RPMS/repodata/*"
```

## Checking that all RPMs install ok

```console
docker run --rm lambci/yumda:2 bash -c "yum list available | tail -n +3 | grep -o -E '^\S+' | grep -v libcrypt-nss | xargs yum install -y"
```

