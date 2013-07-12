#!/usr/bin/perl -W

use strict;
use bytes;
use File::Path;

die "did not specify boot img file\n" unless $ARGV[0];

my $bootimgfile = $ARGV[0];

my $slurpvar = $/;
undef $/;
open (BOOTIMGFILE, "$bootimgfile") or die "could not open boot img file: $bootimgfile\n";
binmode(BOOTIMGFILE);
my $bootimg = <BOOTIMGFILE>;
close BOOTIMGFILE;
$/ = $slurpvar;


my($bootMagic, $kernelSize, $kernelLoadAddr, $ram1Size, $ram1LoadAddr, $ram2Size, $ram2LoadAddr, $tagsAddr, $pageSize, $unused1, $unused2, $bootName, $cmdLine, $id) =
	unpack('a8 L L L L L L L L L L a16 a512 a8', $bootimg);
	
$pageSize = 2048;

my($kernelAddr) = $pageSize;
my($kernelSizeInPages) = int(($kernelSize + $pageSize - 1) / $pageSize);

my($ram1Addr) = (1 + $kernelSizeInPages) * $pageSize;

my($ram1) = substr($bootimg, $ram1Addr, $ram1Size);

if (substr($ram1, 0, 2) ne "\x1F\x8B")
{
	die "The boot image does not appear to contain a valid gzip file";
}

open (RAM1FILE, ">$ARGV[0]-ramdisk.cpio.gz");
binmode(RAM1FILE);
print RAM1FILE $ram1 or die;
close RAM1FILE;

if (-e "$ARGV[0]-ramdisk") { 
	rmtree "$ARGV[0]-ramdisk";
	print "\nremoved old directory $ARGV[0]-ramdisk\n";
}

mkdir "$ARGV[0]-ramdisk" or die;
chdir "$ARGV[0]-ramdisk" or die;
system ("gzip -d -c ../$ARGV[0]-ramdisk.cpio.gz | cpio -i");
system ("rm -f ../$ARGV[0]-ramdisk.cpio.gz");
