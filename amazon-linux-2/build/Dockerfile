FROM amazonlinux:2

RUN yum install -y yum-utils rpm-build rpm-sign createrepo gcc make automake sudo passwd vim less

RUN groupadd mock && \
  groupadd mockbuild && \
  adduser -g mock mockbuild && \
  usermod -aG mockbuild mockbuild && \
  usermod -aG wheel mockbuild && \
  sed -i -r 's/^(%wheel.+)ALL$/\1NOPASSWD: ALL/' /etc/sudoers

RUN amazon-linux-extras enable epel php7.3 redis4.0 memcached1.5 ruby2.6 httpd_modules && \
  yum install -y epel-release

RUN ln -s /usr/lib64 /opt/lib && \
  for dir in bin include; do ln -s /usr/$dir /opt/$dir; done

COPY ./rpmmacros /home/mockbuild/.rpmmacros

WORKDIR /tmp

USER mockbuild

