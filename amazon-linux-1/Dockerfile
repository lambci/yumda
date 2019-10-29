FROM amazonlinux:1

RUN yum install -y tar gzip zip findutils && \
  yum clean all && \
  rm -rf /var/cache/yum /var/lib/yum/history

RUN mkdir -p /lambda && \
  curl https://lambci.s3.amazonaws.com/fs/base.tgz | tar -xz -C /lambda && \
  echo 'installroot=/lambda' >> /etc/yum.conf && \
  yum reinstall -y filesystem && \
  yum clean all && \
  rm -rf /lambda/var/cache/yum /lambda/var/lib/yum/history && \
  sed -i -e 's/enabled=1/enabled=0/g' /lambda/etc/yum.repos.d/*.repo

COPY lambda1.repo /lambda/etc/yum.repos.d/

COPY RPM-GPG-KEY-lambci /etc/pki/rpm-gpg/

RUN rpm --root /lambda --import /etc/pki/rpm-gpg/RPM-GPG-KEY-lambci
