---
lang: en
base_href: ../../../
keywords: [Ariel Parra, blog, linux]
description: Ariel Parra linux blog
title: What is Linux?
js: [cookies, language, theme, menu, favicon]
nav_current: 5
blog_current: 3
blog_number: 1
---

  <div class="container">
    <div class="card center">
      <hr>
        ### 1. What is Linux?       
      <hr>
    </div>
  </div>[comment]: <> (container Title)

  <div class="container">
    <div class="card blog justify" id="1">
      <hr>
        <div class="center">
          #### 1.1 Definition
          [⤷](./blog/linux/1/#1){:class="hidden-link"}
        </div>
      <hr>
      <p>It is an open-source monolithic kernel with the <abbr title="GNU is Not Unix Project">GNU</abbr> <abbr title="General Public License version 2">GPLv2</abbr>, used as the base of many operating systems.
      </p>
      <p><mark>What is a monolithic kernel?</mark> The kernel is software that has hardware control,
      manages and optimizes system resources such as RAM allocation, CPU processes,
      drivers, etc. Acting as a bridge between applications and hardware. It is monolithic
      when all system services operate in the system's kernel with syscalls.
      </p>
      <p><mark>What is open-source?</mark> It is software where anyone can see, analyze and therefore 
      modify the source code.
      </p>
      <p><mark>What is the GPLv2?</mark> It is a software license where any modification to the code
      must have the same license and for every binary file that is distributed, there has 
      to be available source code.</p>
    </div>[comment]: <> (container Elements)
    <div class="card blog justify" id="2">
      <hr>
      <div class="center">
        #### 1.2 History
        [⤷](./blog/linux/1/#2){:class="hidden-link"}
      </div>
      <hr>
      <p>It was created in 1991 by the student of the University of Helsinki Linus Torvalds.
      </p>
      <p>At the same time Richard Stallman along with his GNU project of the <abbr title="Free Software Foundation">FSF</abbr> had already created the applications and utilities of an operating
      system.
      </p>
      <p>These applications and utilities were added to the Linux kernel to create a complete
      system called GNU/Linux.
      </p>
    </div>[comment]: <> (container Elements)
    <div class="card blog justify" id="3">
      <hr>
      <div class="center">
        #### 1.3 Philosophy
        [⤷](./blog/linux/1/#3){:class="hidden-link"}
      </div>
      <hr>
      <p>The Linux philosophy is mainly based on UNIX and the open-source philosophies, 
      where Linux is differentiated is by giving full control to the user, giving him the
      freedom to choose, study, modify and distribute any part of his operating system.
      </p>
      <p>The Linux kernel it self, does not have binary blobs, but these are distributed in the
      Linux-firmware, this serves to initialize the hardware and drivers.
      </p>
      <p>Linux has standards such as the LSB (Linux Standard Base) that define system
      interfaces and run times from where libraries and applications depend. Linux
      operating systems often use the Filesystem Hierarchy Standard of linux.
      </p>
    </div>[comment]: <> (container Elements)
    <div class="card blog justify" id="4">
      <hr>
      <div class="center">
        #### 1.4 Cross Platform
        [⤷](./blog/linux/1/#4){:class="hidden-link"}
      </div>
      <hr>  
      <p>There are four main ways to use Linux, these are: </p>
      <p><mark>Bare Metal:</mark> When the operating system is installed directly on a device that 
      allows you to install operating systems, such as desktop computers, laptops, netbooks, single board computers such as Raspberry Pi's, among others devices like:</p>
    
        - Game Consoles:  [Amiga](http://www.linux-m68k.org/faq/amigahw.html), [N64](https://github.com/clbr/n64bootloader), [sega Dreamcast](https://linuxdc.sourceforge.net/), [GameCube](www.gc-linux.org/), [Wii](https://neagix.github.io/wii-linux-ngx/), [WiiU](https://gitlab.com/linux-wiiu/linux-wiiu), [Nintendo Switch](https://switchroot.org/), [PS1](https://en.wikipedia.org/wiki/PSXLinux), [PS2](https://en.wikipedia.org/wiki/Linux_for_PlayStation_2), [PS3](https://en.wikipedia.org/wiki/OtherOS), [PS4](https://github.com/ps4gentoo/ps4gentoo.github.io), [OG-Xbox](https://en.wikipedia.org/wiki/Xbox_Linux), [Xbox360](https://en.wikipedia.org/wiki/Free60), [Atari CVS](https://web.archive.org/web/20210103170712/https://shop.atarivcs.com/content/Linux-Install-Guide.pdf).
        
        - Portable Game Consoles: [DS](https://www.dslinux.org/index.html), [3DS](https://github.com/linux-3ds), [PSP](https://psplinux.info/2011/09/how-to-use-uclinux-on-the-psp-jackson-mos-port/), [PSVita](https://github.com/xerpi/vita-linux-loader).
        - Smartphones/tablets: [iPhone 7](https://www.xda-developers.com/apple-iphone-7-ubuntu-linux-checkra1n-project-sandcastle/), [iPad 1](https://github.com/chriskmanx/qmole), [Ubuntu Touch](https://ubuntu-touch.io/), [postmarketOS](https://postmarketos.org/).

      <p><mark>Virtualization:</mark> It is a process in which by using software a layer of hardware abstraction is made, allowing the host system resources to be used into virtual machines, limited by the processor's ability to only virtualize operating systems for the same type of processor. Virtualization software examples:</p>
      
        - [VirtualBox](https://www.virtualbox.org/), [VMware Workstation Player](https://www.vmware.com/products/workstation-player.html), [Qemu for Android 13](https://www.esper.io/blog/android-dessert-bites-13-virtualization-on-pixel-6-379185), [crostini for ChromeOs](https://www.chromium.org/chromium-os/developer-library/guides/containers/containers-and-vms/#Crostini), [UTM for MacOS](https://docs.getutm.app/installation/macos/), [Parallels for MacOS](https://www.parallels.com/products/desktop/).
      
      <p><mark>Emulation:</mark> Unlike virtualization, it does not use all the host system resources, it mostly uses the processor to simulate some other processor architecture, although this makes it less efficient. Some emulation software examples: </p>
      
        - [UTMSE/UTM for iOS](https://docs.getutm.app/installation/ios/), [iSH for iOS](https://ish.app/), [JSLinux](https://bellard.org/jslinux/), [copy.sh](https://copy.sh), [QEMU](https://www.qemu.org/), [box86](https://box86.org/).
      
      <p><mark>Containers:</mark> It is a process that is mainly used in systems which already have the Linux kernel, there are various ways to contain a linux environment, like: cgroups, namespaces, docker containers and chroots. Additionally, the X server or VNC protocols can be used to transmit the image from the host and for VNC another application is used as a client to view and interact with the graphical interface.</p>
      
        - Chroot for ChromeOS: [crouton](https://github.com/dnschneid/crouton)
        - Proot on Android: [Termux](https://termux.dev/en/), [Termux Desktop](https://github.com/adi1090x/termux-desktop), [UserLand](https://github.com/CypherpunkArmory/UserLAnd), [Linux Deploy](https://github.com/meefik/linuxdeploy), [AndroNix](https://github.com/AndronixApp/AndronixOrigin).
        - Grafical sessions on Android: [ termux-X11](https://github.com/termux/termux-x11), [multiVNC](https://github.com/bk138/multivnc/), [avnc](https://github.com/gujjwal00/avnc).
    </div>[comment]: <> (container Elements)
  </div>[comment]: <> (container)
  <div class="container">
    <div class="card center" id="References">
      <hr>
        <h3 title="With APA format">References</h3>
        [⤷](./blog/linux/1/#References){:class="hidden-link"}
      <hr>
    </div>
  </div>[comment]: <> (container Title)
  <div class="container">
    <div class="card blog">
        - Britannica, T. Editors of Encyclopaedia (2023). *Linux*. Encyclopedia Britannica. [https://www.britannica.com/technology/Linux](https://www.britannica.com/technology/Linux)
        - David Both. (2014). *The impact of the Linux philosophy*.[ https://opensource.com/business/14/12/linux-philosophy](https://opensource.com/business/14/12/linux-philosophy)
        - Eric Steven Raymond. (2003). *Basics of the Unix Philosophy*. [http://www.catb.org/~esr/writings/taoup/html/ch01s06.html](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html)
        - Fireship. (2022). *Linux in 100 Seconds *[Video]. YouTube. [https://yewtu.be/watch?v=rrB13utjYV4](https://yewtu.be/watch?v=rrB13utjYV4)
        - GeeksforGeeks. (2019). *Linux Tutorials | Getting Started | Introduction | GeeksforGeeks* [Video]. [https://www.youtube.com/watch?v=0EDwEQoui_g&t=213](https://www.youtube.com/watch?v=0EDwEQoui_g&t=213)
        - GNU. (2023). *GNU General Public License, version 2*. Retrieved from [https://www.gnu.org/licenses/old-licenses/gpl-2.0.html](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
        - Google. (n.d.).  *What are Containers?*. Retrieved from [https://cloud.google.com/learn/what-are-containers](https://cloud.google.com/learn/what-are-containers)
        - IBM. (n.d.). *What are Containers?*. Retrieved from [https://www.ibm.com/topics/containers](https://www.ibm.com/topics/containers)
        - IBM. (n.d.). *What is virtualization?*. Retrieved from [https://www.ibm.com/topics/virtualization](https://www.ibm.com/topics/virtualization)
        - Ipadlinux. (2023). *Linux on iPad*. Retrieved from [https://ipadlinux.org/](https://ipadlinux.org/)
        - Linus Torvalds. (1997). *Linux: a Portable Operating System*. Retrieved from [https://www.cs.helsinki.fi/u/kutvonen/index_files/linus.pdf](https://www.cs.helsinki.fi/u/kutvonen/index_files/linus.pdf)
        - Machtelt Garrels. (2008). *Introduction to Linux*. Retrieved from [https://tldp.org/LDP/intro-linux/intro-linux.pdf](https://tldp.org/LDP/intro-linux/intro-linux.pdf)
        - Opensource.com. (n.d.). *What is Linux?*. Retrieved from [https://opensource.com/resources/linux](https://opensource.com/resources/linux)
        - Opensource.com. (n.d.). *What is open source?*. Retrieved from [https://opensource.com/resources/what-open-source](https://opensource.com/resources/what-open-source)
        - Open Source Initiative. (2007). *The Open Source Definition*. Retrieved from [https://opensource.org/osd/](https://opensource.org/osd/)
        - PS4linux.com. (2022). *PS4 Linux Downloads*. Retrieved from [https://ps4linux.com/downloads/](https://ps4linux.com/downloads/)
        - QEMU. (n.d.). *Emulation*. Retrieved from [https://www.qemu.org/docs/master/about/emulation.html](https://www.qemu.org/docs/master/about/emulation.html)
        - Red Hat. (2023). *Understanding containers*. Retrieved from [https://www.redhat.com/en/topics/containers](https://www.redhat.com/en/topics/containers)
        - Red Hat. (2019). *What is the Linux kernel?*. Retrieved from [https://www.redhat.com/en/topics/linux/what-is-the-linux-kernel](https://www.redhat.com/en/topics/linux/what-is-the-linux-kernel)
        - Roch, B. (2004). *Monolithic kernel vs. Microkernel*. Retrieved from [https://web.cs.wpi.edu/~cs3013/c12/Papers/Roch_Microkernels.pdf](https://web.cs.wpi.edu/~cs3013/c12/Papers/Roch_Microkernels.pdf)
        - The Linux Information Project. (2006). *What is Linux?*. [http://www.linfo.org/newbies.html](http://www.linfo.org/newbies.html)
        - The Linux Kernel Organization. (2022). *About Linux Kernel*. Retrieved from [https://www.kernel.org/linux.html](https://www.kernel.org/linux.html)
        - The Linux Kernel Organization. (2022). *Is Linux Kernel Free Software?*. Retrieved from [https://www.kernel.org/category/faq.html](https://www.kernel.org/category/faq.html)
        - Wheeler, D. (2003). *History of Unix, Linux, and Open Source / Free Software*. Retrieved from [https://tldp.org/HOWTO/Secure-Programs-HOWTO/history.html](https://tldp.org/HOWTO/Secure-Programs-HOWTO/history.html)
      <p class="center">
        Last update on: February 7th 2024.
      </p>
    </div>[comment]: <> (container Elements)
  </div>[comment]: <> (container)
  