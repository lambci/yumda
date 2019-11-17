FROM amazonlinux:1

RUN yum install -y shadow-utils yum-utils rpm-build rpm-sign createrepo gcc gcc-c++ make automake sudo passwd vim less epel-release

RUN groupadd mock && \
  groupadd mockbuild && \
  adduser -g mock mockbuild && \
  usermod -aG mockbuild mockbuild && \
  usermod -aG wheel mockbuild && \
  sed -i -r 's/^# (%wheel.+NOPASSWD: ALL)$/\1/' /etc/sudoers

RUN yum-config-manager --enable epel

RUN ln -s /usr/lib64 /opt/lib && \
  for dir in bin include; do ln -s /usr/$dir /opt/$dir; done

WORKDIR /tmp

COPY ./*.patch ./
RUN for file in *.patch; do patch -d/ -p0 < $file; done && rm *.patch

USER mockbuild

COPY ./rpmmacros /home/mockbuild/.rpmmacros
