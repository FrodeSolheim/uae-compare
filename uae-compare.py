#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
#from __future__ import unicode_literals

import os
import sys
import shutil
import subprocess
from projects import projects

indenter = "astyle"


def fix_file(path):
    with open(path, "rb") as f:
        data = f.read()
    for header_file in uae_header_files:
        #print('#include "{0}"'.format(header_file))
        n, e = os.path.splitext(header_file)
        data = data.replace('include "{0}"'.format(header_file),
                            'include "uae/{0}"'.format(header_file))
        data = data.replace('include "{0}_uae.h"'.format(n),
                            'include "uae/{0}"'.format(header_file))
    if options["no-blank-lines"]:
        while "\n\n" in data:
            data = data.replace("\n\n", "\n")
    data = data.strip() + "\n"
    with open(path, "wb") as f:
        f.write(data)


def format_project(project, src_dir, dst_dir):
    for src_name, dst_name in file_map.items():
        src_path = os.path.join(src_dir, src_name)
        dst_path = os.path.join(dst_dir, dst_name)
        #print((src_path), os.path.exists(src_path))
        if not os.path.exists(src_path):
            continue
        if not os.path.exists(os.path.dirname(dst_path)):
            os.makedirs(os.path.dirname(dst_path))
        shutil.copy(src_path, dst_path)

    for dir_path, dir_names, file_names in os.walk(dst_dir):
        for name in file_names:
            path = os.path.join(dir_path, name)
            if path.endswith(".c") or path.endswith(".h"):
                if indenter == "astyle":
                    args = ["astyle", "--options=astylerc", path]
                    if options["no-blank-lines"]:
                        args.insert(1, "--delete-empty-lines")
                elif indenter == "uncrustify":
                    args = ["uncrustify", "-c", "uncrustify.cfg", path]
                #print(args)
                assert subprocess.Popen(args).wait() == 0
                if os.path.exists(path + ".orig"):
                    os.remove(path + ".orig")
                fix_file(path)


source_files = [
    "a2065.cpp",
    "a2091.cpp",
    "adide.cpp",
    "akiko.cpp",
    "amax.cpp",
    "arcadia.cpp",
    "ar.cpp",
    "audio.cpp",
    "autoconf.cpp",
    "blitops.cpp",
    "blitter.cpp",
    "blkdev_cdimage.cpp",
    "blkdev.cpp",
    "bsdsocket.cpp",
    "build68k.cpp",
    "calc.cpp",
    "catweasel.cpp",
    "cd32_fmv.cpp",
    "cdrom.cpp",
    "cdrom-handler.cpp",
    "cdtv.cpp",
    "cfgfile.cpp",
    "cia.cpp",
    "consolehook.cpp",
    "core.cw4.cpp",
    "cpummu.cpp",
    "cpuopti.cpp",
    "crc32.cpp",
    "custom.cpp",
    "debug.cpp",
    "disk.cpp",
    "diskutil.cpp",
    "dongle.cpp",
    "drawing.cpp",
    "driveclick.cpp",
    "enforcer.cpp",
    "epsonprinter.cpp",
    "events.cpp",
    "expansion.cpp",
    "fdi2raw.cpp",
    "filesys.asm",
    "filesys_bootrom.cpp",
    "filesys.cpp",
    "filesys.sh",
    "fpp.cpp",
    "fsdb.cpp",
    # "fsdb_unix.cpp",
    "fsusage.cpp",
    "gayle.cpp",
    "genblitter.cpp",
    "gencpu.cpp",
    # "gencpu_mini.cpp",
    "gengenblitter.cpp",
    "genlinetoscr.cpp",
    "genp2c.cpp",
    "gfxboard.cpp",
    "gfxlib.cpp",
    "gfxutil.cpp",
    # "gtkui.cpp",
    "hardfile.cpp",
    "hrtmon.rom.cpp",
    "identify.cpp",
    "inprec.cpp",
    "inputdevice.cpp",
    "inputevents.def",
    "inputrecord.cpp",
    "isofs.cpp",
    "keybuf.cpp",
    "luascript.cpp",
    "main.cpp",
    "memory.cpp",
    "missing.cpp",
    "moduleripper.cpp",
    "native2amiga.cpp",
    "ncr_scsi.cpp",
    "newcpu.cpp",
    "nogui.cpp",
    "p96_blit.cpp",
    # FS-UAE and WinUAE have od-xxx/... and PUAE picasso96.c
    # "picasso96.cpp",
    "readcpu.cpp",
    "readdisk.cpp",
    "rommgr.cpp",
    "rpc.cpp",
    "sampler.cpp",
    "sana2.cpp",
    "savestate.cpp",
    "scsi.cpp",
    "scsidev.cpp",
    "scsiemul.cpp",
    "serial.cpp",
    "sinctable.cpp",
    "specialmonitors.cpp",
    "statusline.cpp",
    "table68k",
    "traps.cpp",
    "uaeexe.cpp",
    "uaeipc.cpp",
    "uaelib.cpp",
    "uaeresource.cpp",
    "uaeserial.cpp",
    "uaeunp.cpp",
    "writelog.cpp",
    "zfile_archive.cpp",
    "zfile.cpp",
]


file_map = {
    # WinUAE & FS-UAE JIT files
    "jit/codegen_x86.cpp": "jit/codegen_x86.c",
    "jit/codegen_x86.h": "jit/codegen_x86.h",
    "jit/compemu_codegen.h": "jit/compemu_codegen.h",
    "jit/compemu_fpp.cpp": "jit/compemu_fpp.c",
    "jit/compemu.h": "jit/compemu.h",
    "jit/compemu_optimizer_x86.cpp": "jit/compemu_optimizer_x86.c",
    "jit/compemu_raw_x86.cpp": "jit/compemu_raw_x86.c",
    "jit/compemu_support_codegen.cpp": "jit/compemu_support_codegen.c",
    "jit/compemu_support.cpp": "jit/compemu_support.c",
    "jit/gencomp.cpp": "jit/gencomp.c",

    # PUAE JIT files
    "codegen_x86.c": "jit/codegen_x86.c",
    "codegen_x86.h": "jit/codegen_x86.h",
    "compemu_codegen.h": "jit/compemu_codegen.h",
    "compemu_fpp.c": "jit/compemu_fpp.c",
    "compemu.h": "jit/compemu.h",
    "compemu_optimizer_x86.c": "jit/compemu_optimizer_x86.c",
    "compemu_raw_x86.c": "jit/compemu_raw_x86.c",
    "compemu_support_codegen.c": "jit/compemu_support_codegen.c",
    "compemu_support.c": "jit/compemu_support.c",
    "gencomp.c": "jit/gencomp.c",

    # PUAE files
    "picasso96.c": "od/picasso96.c",
    "include/memory_uae.h": "include/memory.h",

    # FS-UAE files
    "od-fs/ahidsound.cpp": "od/ahidsound_new.c",
    "od-fs/ahidsound.h": "od/ahidsound.h",
    "od-fs/ahidsound_new.h": "od/ahidsound_new.h",
    "od-fs/mman.cpp": "od/mman.c",
    "od-fs/parser.cpp": "od/parser.c",
    "od-fs/picasso96.cpp": "od/picasso96.c",
    "od-fs/picasso96_host.h": "od/picasso96.h",
    "include/uae/memory.h": "include/memory.h",

    # WinUAE files
    "od-win32/ahidsound.h": "od/ahidsound.h",
    "od-win32/ahidsound_new.cpp": "od/ahidsound_new.c",
    "od-win32/ahidsound_new.h": "od/ahidsound_new.h",
    "od-win32/mman.cpp": "od/mman.c",
    "od-win32/parser.cpp": "od/parser.c",
    "od-win32/picasso96_win.cpp": "od/picasso96.c",
    "od-win32/picasso96_win.h": "od/picasso96.h",
}

for name in source_files:
    file_map[name] = name[:-2]
    file_map[name[:-2]] = name[:-2]

uae_header_files = [
    "a2065.h",
    "a2091.h",
    "akiko.h",
    "amax.h",
    "arcadia.h",
    "ar.h",
    "audio.h",
    "autoconf.h",
    "blitter.h",
    "blkdev.h",
    "bsdsocket.h",
    "calc.h",
    "catweasel.h",
    "cd32_fmv.h",
    "cdtv.h",
    "cia.h",
    "clipboard.h",
    "commpipe.h",
    "consolehook.h",
    "cpummu.h",
    "cpu_prefetch.h",
    "crc32.h",
    "custom.h",
    "debug.h",
    "disk.h",
    "diskutil.h",
    "dongle.h",
    "drawing.h",
    "driveclick.h",
    "enforcer.h",
    "epsonprinter.h",
    "ersatz.h",
    "events.h",
    "events_normal.h",
    "execio.h",
    "execlib.h",
    "fdi2raw.h",
    "filesys.h",
    "flags_x86.h",
    "fpp-ieee-be.h",
    "fpp-unknown.h",
    "fsdb.h",
    "fsusage.h",
    "gayle.h",
    "genblitter.h",
    "gensound.h",
    "gfxfilter.h",
    "gui.h",
    "identify.h",
    "inputdevice.h",
    "inputrecord.h",
    "isofs_api.h",
    "isofs.h",
    "keyboard.h",
    "keybuf.h",
    "mackbd.h",
    "memory.h",
    "moduleripper.h",
    "native2amiga_api.h",
    "native2amiga.h",
    "ncr_scsi.h",
    "newcpu.h",
    "options.h",
    "osemu.h",
    "parallel.h",
    "picasso96.h",
    "readcpu.h",
    "rommgr.h",
    "rtgmodes.h",
    "sampler.h",
    "sana2.h",
    "savestate.h",
    "scsidev.h",
    "scsi.h",
    "serial.h",
    "statusline.h",
    "sysdeps.h",
    "traps.h",
    "uaeexe.h",
    "uae.h",
    "uaeipc.h",
    "uaeresource.h",
    "uaeserial.h",
    "xwin.h",
    "zarchive.h",
    "zfile.h",
]

for name in uae_header_files:
    file_map["include/" + name] = "include/" + name

options = {
    "no-blank-lines": "--no-blank-lines" in sys.argv,
}

for project, src_dir in projects.items():
    if not os.path.exists(src_dir) and \
            os.path.exists(os.path.join("..", src_dir)):
        old_src_dir = src_dir
        src_dir = os.path.join("..", src_dir)
        print("using", src_dir, "instead of", old_src_dir)

    dst_dir = project
    format_project(project, src_dir, dst_dir)
