#!/usr/bin/perl

# This is a sample Script file
# It does not much:
#   * Loading configuration
#   * including header.htmlfooter.html
#   * and showing a message to the user.
# That's all.

use File::HomeDir;
use CGI qw/:standard/;
use Config::Simple;
use Cwd 'abs_path';
use IO::Socket::INET;
use HTML::Entities;
use String::Escape qw( unquotemeta );
use warnings;
use strict;
no strict "refs"; # we need it for template system
use LoxBerry::System;

my  $home = File::HomeDir->my_home;
our $lang;
my  $installfolder;
my  $cfg;
my  $conf;
our $psubfolder;
our $template_title;
our $namef;
our $value;
our %query;
our $phrase;
our $phraseplugin;
our $languagefile;
our $languagefileplugin;
our $cache;
our $savedata;
our $MSselectlist;
our $username;
our $password;
our $miniserver;
our $msudpport;
our $enabled;
our $enabledlist;
our $enabledusb1;
our $enabledusblist1;
our $enabledusb2;
our $enabledusblist2;
our $enabledusb3;
our $enabledusblist3;
our $enabledusb4;
our $enabledusblist4;
our $usb1id;
our $usb2id;
our $usb3id;
our $usb4id;
our $listdevice;
our $restartscript;
my $confusb;
our $usb1;
our $usb2;
our $usb3;
our $usb4;
our $usb1baud;
our $usb2baud;
our $usb3baud;
our $usb4baud;
our $usb1port;
our $usb2port;
our $usb3port;
our $usb4port;
our $faultport12;
our $faultport13;
our $faultport14;
our $faultport23;
our $faultport24;
our $faultport34;
our $faultport;
our $faultportxx;
our $usb1praefix;
our $usb2praefix;
our $usb3praefix;
our $usb4praefix;
our $loglv;
our $Loglevellist;


# ---------------------------------------
# Read Settings
# ---------------------------------------
$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");


print "Content-Type: text/html\n\n";

# ---------------------------------------
# Parse URL
# ---------------------------------------
foreach (split(/&/,$ENV{"QUERY_STRING"}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# ---------------------------------------
# Set parameters coming in - GET over POST
# ---------------------------------------

if ( !$query{'miniserver'} )   { if ( param('miniserver')  ) { $miniserver = quotemeta(param('miniserver'));         } 
else { $miniserver = $miniserver;  } } else { $miniserver = quotemeta($query{'miniserver'});   }

if ( !$query{'msudpport'} )   { if ( param('msudpport')  ) { $msudpport = quotemeta(param('msudpport'));         } 
else { $msudpport = $msudpport;  } } else { $msudpport = quotemeta($query{'msudpport'});   }	

if ( !$query{'enabled'} )   { if ( param('enabled')  ) { $enabled = quotemeta(param('enabled'));         } 
else { $enabled = $enabled;  } } else { $enabled = quotemeta($query{'enabled'});   }

if ( !$query{'enabledusb1'} )   { if ( param('enabledusb1')  ) { $enabledusb1 = quotemeta(param('enabledusb1'));         } 
else { $enabledusb1 = $enabledusb1;  } } else { $enabledusb1 = quotemeta($query{'enabledusb1'});   }

if ( !$query{'enabledusb2'} )   { if ( param('enabledusb2')  ) { $enabledusb2 = quotemeta(param('enabledusb2'));         } 
else { $enabledusb2 = $enabledusb2;  } } else { $enabledusb2 = quotemeta($query{'enabledusb2'});   }

if ( !$query{'enabledusb3'} )   { if ( param('enabledusb3')  ) { $enabledusb3 = quotemeta(param('enabledusb3'));         } 
else { $enabledusb3 = $enabledusb3;  } } else { $enabledusb3 = quotemeta($query{'enabledusb3'});   }

if ( !$query{'enabledusb4'} )   { if ( param('enabledusb4')  ) { $enabledusb4 = quotemeta(param('enabledusb4'));         } 
else { $enabledusb4 = $enabledusb4;  } } else { $enabledusb4 = quotemeta($query{'enabledusb4'});   }

if ( !$query{'usb1id'} )   { if ( param('usb1id')  ) { $usb1id = quotemeta(param('usb1id'));         } 
else { $usb1id = $usb1id;  } } else { $usb1id = quotemeta($query{'usb1id'});   }

if ( !$query{'usb2id'} )   { if ( param('usb2id')  ) { $usb2id = quotemeta(param('usb2id'));         } 
else { $usb2id = $usb2id;  } } else { $usb2id = quotemeta($query{'usb2id'});   }

if ( !$query{'usb3id'} )   { if ( param('usb3id')  ) { $usb3id = quotemeta(param('usb3id'));         } 
else { $usb3id = $usb3id;  } } else { $usb3id = quotemeta($query{'usb3id'});   }

if ( !$query{'usb4id'} )   { if ( param('usb4id')  ) { $usb4id = quotemeta(param('usb4id'));         } 
else { $usb4id = $usb4id;  } } else { $usb4id = quotemeta($query{'usb4id'});   }

if ( !$query{'usb1baud'} )   { if ( param('usb1baud')  ) { $usb1baud = quotemeta(param('usb1baud'));         } 
else { $usb1baud = $usb1baud;  } } else { $usb1baud = quotemeta($query{'usb1baud'});   }

if ( !$query{'usb2baud'} )   { if ( param('usb2baud')  ) { $usb2baud = quotemeta(param('usb2baud'));         } 
else { $usb2baud = $usb2baud;  } } else { $usb2baud = quotemeta($query{'usb2baud'});   }

if ( !$query{'usb3baud'} )   { if ( param('usb3baud')  ) { $usb3baud = quotemeta(param('usb3baud'));         } 
else { $usb3baud = $usb3baud;  } } else { $usb3baud = quotemeta($query{'usb3baud'});   }

if ( !$query{'usb4baud'} )   { if ( param('usb4baud')  ) { $usb4baud = quotemeta(param('usb4baud'));         } 
else { $usb4baud = $usb4baud;  } } else { $usb4baud = quotemeta($query{'usb4baud'});   }

if ( !$query{'usb1port'} )   { if ( param('usb1port')  ) { $usb1port = quotemeta(param('usb1port'));         } 
else { $usb1port = $usb1port;  } } else { $usb1port = quotemeta($query{'usb1port'});   }

if ( !$query{'usb2port'} )   { if ( param('usb2port')  ) { $usb2port = quotemeta(param('usb2port'));         } 
else { $usb2port = $usb2port;  } } else { $usb2port = quotemeta($query{'usb2port'});   }

if ( !$query{'usb3port'} )   { if ( param('usb3port')  ) { $usb3port = quotemeta(param('usb3port'));         } 
else { $usb3port = $usb3port;  } } else { $usb3port = quotemeta($query{'usb3port'});   }

if ( !$query{'usb4port'} )   { if ( param('usb4port')  ) { $usb4port = quotemeta(param('usb4port'));         } 
else { $usb4port = $usb4port;  } } else { $usb4port = quotemeta($query{'usb4port'});   }

if ( !$query{'usb1praefix'} )   { if ( param('usb1praefix')  ) { $usb1praefix = quotemeta(param('usb1praefix'));         } 
else { $usb1praefix = $usb1praefix;  } } else { $usb1praefix = quotemeta($query{'usb1praefix'});   }

if ( !$query{'usb2praefix'} )   { if ( param('usb2praefix')  ) { $usb2praefix = quotemeta(param('usb2praefix'));         } 
else { $usb2praefix = $usb2praefix;  } } else { $usb2praefix = quotemeta($query{'usb2praefix'});   }

if ( !$query{'usb3praefix'} )   { if ( param('usb3praefix')  ) { $usb3praefix = quotemeta(param('usb3praefix'));         } 
else { $usb3praefix = $usb3praefix;  } } else { $usb3praefix = quotemeta($query{'usb3praefix'});   }

if ( !$query{'usb4praefix'} )   { if ( param('usb4praefix')  ) { $usb4praefix = quotemeta(param('usb4praefix'));         } 
else { $usb4praefix = $usb4praefix;  } } else { $usb4praefix = quotemeta($query{'usb4praefix'});   }

if ( !$query{'loglv'} )   { if ( param('loglv')  ) { $loglv = quotemeta(param('loglv'));         } 
else { $loglv = $loglv;  } } else { $loglv = quotemeta($query{'loglv'});   }


# ---------------------------------------
# Figure out in which subfolder we are installed
# ---------------------------------------
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;


# ---------------------------------------
# Save settings to config file
# ---------------------------------------
if (param('savedata')) {
	$conf = new Config::Simple("$home/config/plugins/$psubfolder/serialusb-bridge-config.cfg");

	if ($enabled ne 1) { $enabled = 0 }

	$username = encode_entities($username);
	print STDERR "$username\n";

	$conf->param('serialusbbridge-config.MINISERVER', unquotemeta("MINISERVER$miniserver"));
	$conf->param('serialusbbridge-config.UDPPORT', unquotemeta($msudpport));
	$conf->param('serialusbbridge-config.ENABLED', unquotemeta($enabled));
	$conf->param('serialusbbridge-config.ENABLEDUSB1', unquotemeta($enabledusb1));
	$conf->param('serialusbbridge-config.ENABLEDUSB2', unquotemeta($enabledusb2));
	$conf->param('serialusbbridge-config.ENABLEDUSB3', unquotemeta($enabledusb3));
	$conf->param('serialusbbridge-config.ENABLEDUSB4', unquotemeta($enabledusb4));
	$conf->param('serialusbbridge-config.USB1ID', unquotemeta($usb1id));
	$conf->param('serialusbbridge-config.USB2ID', unquotemeta($usb2id));
	$conf->param('serialusbbridge-config.USB3ID', unquotemeta($usb3id));
	$conf->param('serialusbbridge-config.USB4ID', unquotemeta($usb4id));
	$conf->param('serialusbbridge-config.USB1BAUD', unquotemeta($usb1baud));
	$conf->param('serialusbbridge-config.USB2BAUD', unquotemeta($usb2baud));
	$conf->param('serialusbbridge-config.USB3BAUD', unquotemeta($usb3baud));
	$conf->param('serialusbbridge-config.USB4BAUD', unquotemeta($usb4baud));
	$conf->param('serialusbbridge-config.USB1PORT', unquotemeta($usb1port));
	$conf->param('serialusbbridge-config.USB2PORT', unquotemeta($usb2port));
	$conf->param('serialusbbridge-config.USB3PORT', unquotemeta($usb3port));
	$conf->param('serialusbbridge-config.USB4PORT', unquotemeta($usb4port));
	$conf->param('serialusbbridge-config.USB1PRAEFIX', unquotemeta($usb1praefix));
	$conf->param('serialusbbridge-config.USB2PRAEFIX', unquotemeta($usb2praefix));
	$conf->param('serialusbbridge-config.USB3PRAEFIX', unquotemeta($usb3praefix));
	$conf->param('serialusbbridge-config.USB4PRAEFIX', unquotemeta($usb4praefix));
	$conf->param('serialusbbridge-config.LOGLV', unquotemeta($loglv));
	reboot_required("Please Restart after the reboot the Script in the Plugin");
	
	$conf->save();

}
#bei Abfrage die liste erneuern
if (param('listdevice')) {

system('ID=$((ID=1)); echo -n >'.$home.'/config/plugins/'.$psubfolder.'/listofusb.cfg; for file in /dev/serial/by-id/*; do echo "USB$ID=$file" >> '.$home.'/config/plugins/'.$psubfolder.'/listofusb.cfg; ID=$((ID+1)); done;');

}

if(param('restartscript')){
system('python3 '.$home.'/bin/plugins/'.$psubfolder.'/restart.py &');
}
# ---------------------------------------
# Parse config file usb geräte
# ---------------------------------------
$confusb = new Config::Simple("$home/config/plugins/$psubfolder/listofusb.cfg");
$usb1 = $confusb->param('USB1');
$usb2 = $confusb->param('USB2');
$usb3 = $confusb->param('USB3');
$usb4 = $confusb->param('USB4');

# ---------------------------------------
# Parse config file
# ---------------------------------------
$conf = new Config::Simple("$home/config/plugins/$psubfolder/serialusb-bridge-config.cfg");
$miniserver = encode_entities($conf->param('serialusbbridge-config.MINISERVER'));
$msudpport = encode_entities($conf->param('serialusbbridge-config.UDPPORT'));
$enabled = encode_entities($conf->param('serialusbbridge-config.ENABLED'));
$enabledusb1 = encode_entities($conf->param('serialusbbridge-config.ENABLEDUSB1'));
$enabledusb2 = encode_entities($conf->param('serialusbbridge-config.ENABLEDUSB2'));
$enabledusb3 = encode_entities($conf->param('serialusbbridge-config.ENABLEDUSB3'));
$enabledusb4 = encode_entities($conf->param('serialusbbridge-config.ENABLEDUSB4'));
$usb1id = encode_entities($conf->param('serialusbbridge-config.USB1ID'));
$usb2id = encode_entities($conf->param('serialusbbridge-config.USB2ID'));
$usb3id = encode_entities($conf->param('serialusbbridge-config.USB3ID'));
$usb4id = encode_entities($conf->param('serialusbbridge-config.USB4ID'));
$usb1baud = encode_entities($conf->param('serialusbbridge-config.USB1BAUD'));
$usb2baud = encode_entities($conf->param('serialusbbridge-config.USB2BAUD'));
$usb3baud = encode_entities($conf->param('serialusbbridge-config.USB3BAUD'));
$usb4baud = encode_entities($conf->param('serialusbbridge-config.USB4BAUD'));
$usb1port = encode_entities($conf->param('serialusbbridge-config.USB1PORT'));
$usb2port = encode_entities($conf->param('serialusbbridge-config.USB2PORT'));
$usb3port = encode_entities($conf->param('serialusbbridge-config.USB3PORT'));
$usb4port = encode_entities($conf->param('serialusbbridge-config.USB4PORT'));
$usb1praefix = encode_entities($conf->param('serialusbbridge-config.USB1PRAEFIX'));
$usb2praefix = encode_entities($conf->param('serialusbbridge-config.USB2PRAEFIX'));
$usb3praefix = encode_entities($conf->param('serialusbbridge-config.USB3PRAEFIX'));
$usb4praefix = encode_entities($conf->param('serialusbbridge-config.USB4PRAEFIX'));
$loglv = encode_entities($conf->param('serialusbbridge-config.LOGLV'));


# ---------------------------------------
# Set Enabled / Disabled switch
# ---------------------------------------
if ($enabled eq "1") {
	$enabledlist = '<option value="0">Nein</option><option value="1" selected>JA</option>\n';
} else {
	$enabledlist = '<option value="0" selected>Nein</option><option value="1">JA</option>\n';
}

if ($enabledusb1 eq "1") {
	$enabledusblist1 = '<option value="0">Nein</option><option value="1" selected>JA</option>\n';
} else {
	$enabledusblist1 = '<option value="0" selected>Nein</option><option value="1">JA</option>\n';
}

if ($enabledusb2 eq "1") {
	$enabledusblist2 = '<option value="0">Nein</option><option value="1" selected>JA</option>\n';
} else {
	$enabledusblist2 = '<option value="0" selected>Nein</option><option value="1">JA</option>\n';
}

if ($enabledusb3 eq "1") {
	$enabledusblist3 = '<option value="0">Nein</option><option value="1" selected>JA</option>\n';
} else {
	$enabledusblist3 = '<option value="0" selected>Nein</option><option value="1">JA</option>\n';
}

if ($enabledusb4 eq "1") {
	$enabledusblist4 = '<option value="0">Nein</option><option value="1" selected>JA</option>\n';
} else {
	$enabledusblist4 = '<option value="0" selected>Nein</option><option value="1">JA</option>\n';
}

# ---------------------------------------
# Set LOGLEVEL-SWITCH Dropdown
# ---------------------------------------
if ($loglv eq "10") {
	$Loglevellist = '<option value="10" selected>INFO</option><option value="20">WARNING</option><option value="30">ERROR</option>\n';
} 
if ($loglv eq "20"){
	$Loglevellist = '<option value="10">INFO</option><option value="20" selected>WARNING</option><option value="30">ERROR</option>\n';
}
if ($loglv eq "30"){
	$Loglevellist = '<option value="10">INFO</option><option value="20">WARNING</option><option value="30" selected>ERROR</option>\n';
}



# ---------------------------------------
# Fill Miniserver selection dropdown
# ---------------------------------------
for (my $i = 1; $i <= $cfg->param('BASE.MINISERVERS');$i++) {
	if ("MINISERVER$i" eq $miniserver) {
		$MSselectlist .= '<option selected value="'.$i.'">'.$cfg->param("MINISERVER$i.NAME")."</option>\n";
	} else {
		$MSselectlist .= '<option value="'.$i.'">'.$cfg->param("MINISERVER$i.NAME")."</option>\n";
	}
}


# Init Language
	# Clean up lang variable
	$lang         =~ tr/a-z//cd; $lang         = substr($lang,0,2);
  # If there's no language phrases file for choosed language, use german as default
		if (!-e "$installfolder/templates/system/$lang/language.dat") 
		{
  		$lang = "de";
	}
	# Read translations / phrases
		$languagefile 			= "$installfolder/templates/system/$lang/language.dat";
		$phrase 						= new Config::Simple($languagefile);
		$languagefileplugin = "$installfolder/templates/plugins/$psubfolder/$lang/language.dat";
		$phraseplugin 			= new Config::Simple($languagefileplugin);



# Title
$template_title = $phrase->param("1") . "Seriell->USB zu UDP Loxone Bridge";

#----------------------------------------
#Fehlermeldung bei gleichen ports
#----------------------------------------
  if ($usb1port == $usb2port || $usb1port == $msudpport || $usb2port == $msudpport )
{$faultport12 = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=30% height=30%";
}
else {$faultport12 = "";
}
if ($usb1port == $usb3port)
{$faultport13 = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=30% height=30%";
}
else {$faultport13 = "";
}
if ($usb1port == $usb4port)
{$faultport14 = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=30% height=30%";
}
else {$faultport14 = "";
}
if ($usb2port == $usb3port)
{$faultport23 = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=30% height=30%";
}
else {$faultport23 = "";
}
if ($usb2port == $usb4port)
{$faultport24 = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=30% height=30%";
}
else {$faultport24 = "";
}
if ($usb3port == $usb4port || $usb3port == $msudpport || $usb4port == $msudpport )
{$faultport34 = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=30% height=30%";
}
else {$faultport34 = "";
}
if ($usb1port == $usb2port || $usb1port == $usb3port || $usb1port == $usb4port || $usb2port == $usb3port || $usb2port == $usb4port || $usb3port == $usb4port || $usb1port == $msudpport || $usb2port == $msudpport || $usb3port == $msudpport || $usb4port == $msudpport )
{$faultportxx = "<img src=../../../plugins/serialusb-bridge/warning.png alt=test width=5% height=5%";
$faultport = "<font color=#ff0000; >WARUNG ES DARF KEIN PORT DOPPELT BELEGT WERDEN!!! <br> WARNUNG ES DARF NICHT DER PORT DES MINISERVERS VERWENDET WERDEN</font>";
}
else {$faultportxx = "<img src=../../../plugins/serialusb-bridge/ok.png alt=test width=5% height=5%";
$faultport = "<font color=#00fd00; >ALLES OK!!!</font>";
}




# ---------------------------------------
# Load header and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load content from template
# ---------------------------------------
open(F,"$installfolder/templates/plugins/$psubfolder/index.html") || die "Missing template /index.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load footer and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
