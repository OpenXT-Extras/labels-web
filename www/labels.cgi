#!/usr/bin/env perl 
#
# Copyright (c) 2014 Citrix Systems, Inc.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

(my $labels_dir = $0) =~ s/[^\/]*$//;
BEGIN { push @INC, $labels_dir; }

use strict;
use CGI qw/:standard/;
use Data::Dumper;
use Label;

my $width = 62;

if ( !param() ) {

    print header, start_html('Print a label');

    print start_form(
        -method  => 'GET',
        -enctype => 'application/x-www-form-urlencoded'
    );
    print textfield('label'), submit('submit');
    print end_form, end_html;

    exit 0;

}

my $label = param('label');

my $im = Label::Label($label);

my $png = $im->png;

exit 1 unless defined $png;

print "Content-Type: image/png\n\n";
print $png;

open FISH, "|pngtopnm|ppmtopgm|pgmtopbm -thresh | ptouch $width > /dev/usb/lp0";
print FISH $png;
close FISH;

exit 0;

