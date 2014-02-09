#!/usr/bin/perl

use strict vars;

use Getopt::Long;
use Pod::Usage;

my( $serverMachine, %players, %machines, %resources, %matches );
my( $queryProg, $matchProg );
$queryProg = './queryMatch.py';
$matchProg = './matchConstructor.py';


# arguments: matchName
# returns: NONE|FINISHED|RUNNING|ERROR
sub queryStatus
{
    my( $r, @results, $i, @bots, @botSpec );

    $r = `$queryProg --server=$serverMachine $_[0]`;
    ( $? >> \8 ) == 0
	or die "ERROR: could not contact $serverMachine for status";
    while( chomp $r ) {}
    @results = split ":", $r;
    if( $results[ 1 ] eq "NONE" ) {

	return ( "NONE" );
    } elsif( $results[ 2 ] eq "STARTING" ) {

	return "RUNNING";
    } elsif( $results[ 2 ] eq "RUNNING" ) {

	return "RUNNING";
    } elsif( $results[ 2 ] eq "FINISHED" ) {

	return "FINISHED";
    } elsif( $results[ 2 ] eq "ERROR" ) {

	return "ERROR";
    } else {

	die "ERROR: unexpected output from $queryProg: $r";
    }
}

# arguments: $machine
# returns: 1 if resources are available, 0 otherwise
sub checkMachineResources
{
    my( $machine, $i );
    $machine = $_[ 0 ];

    for( $i = 3; $i <= $#{ $machines{ $machine }}; ++$i ) {
	if( $resources{ ${machines{ $machine }}[ $i ] } <= 0 ) {
	    # missing a required resource
	    return 0;
	}
    }

    return 1;
}

# arguments: $machine $count
# add count for each resource used by machine
sub modifyMachineResources
{
    my( $machine, $count, $i );
    $machine = $_[ 0 ];
    $count = $_[ 1 ];

    for( $i = 3; $i <= $#{ $machines{ $machine }}; ++$i ) {
	$resources{ ${machines{ $machine }}[ $i ] } += $count;
    }
}

# arguments: $match $cur_player
# returns a list of machines to use, or empty list on failure
# works recursively, first call should be with player = 0
sub scheduleMatch
{
    my( $match, $player, $machines, $matchRef, $machinesRef );
    my( @retlist, @childlist, $i, $machine );
    $match = $_[ 0 ];
    $player = $_[ 1 ];
    $matchRef = $matches{ $match };
    $machinesRef = $players{ $$matchRef[ $player + 3 ] };

    for( $i = 0; $i <= $#$machinesRef; ++$i ) {
	$machine = $$machinesRef[ $i ];
	if( !defined( $machines{ $machine } ) ) {
	    # machine is already used
	    next;
	}

	if( !checkMachineResources( $machine ) ) {
	    # resources are in use
	    next;
	}

	# looks good
	@retlist = ( $machine );

	if( $player + 3 == $#$matchRef ) {
	    # all players scheduled - success!
	    return @retlist;
	}

	# try booking the resources, then continue to schedule the match
	modifyMachineResources( $machine, -1 );
	@childlist = scheduleMatch( $match, $player + 1 );
	modifyMachineResources( $machine, +1 );
	if( $#childlist >= 0 ) {
	    push @retlist, @childlist;
	    return @retlist;
	}
    }

    return ();
}


my( $man, $help, $playerFile, $machineFile, $matchFile, $transFile );
my( $line, $i, %matchStatus, $matchRef, $queryResult, %unfinishedPlayers );
my( $p, $s, $machinesRef, $m, $machine, @matchMachines, $t, $running );


GetOptions( 'help' => \$help, 'man' => \$man ) 
  or pod2usage( -exitstatus => 2, 
                -message => "Invalid arguments.\n" .
                            "Use --help or --man for detailed usage.");
pod2usage( -verbose => 1 ) if( $help );
pod2usage( -verbose => 2 ) if( $man );
$#ARGV >= 4
  or pod2usage( -exitstatus => 2, 
                -message => "Insufficient arguments.\n" .
                            "Use --help or --man for detailed usage.");

$serverMachine = $ARGV[ 0 ];
$playerFile = $ARGV[ 1 ];
$machineFile = $ARGV[ 2 ];
$matchFile = $ARGV[ 3 ];
$transFile = $ARGV[ 4 ];

# read all the files
open FILE, "<", $playerFile
    or die "ERROR: could not open player file $playerFile";
while( $line = <FILE> ) {
    chomp $line; if( $line eq "" || substr( $line, 0, 1 ) eq "#" ) { next; }
    @_ = split " ", $line;
    !defined( $players{ $_[ 0 ] } )
	or die "ERROR: $_[0] defined in $playerFile multiple times";
    $players{ $_[ 0 ] } = [];
}
close FILE;

open FILE, "<", $machineFile
    or die "ERROR: could not open resource file $machineFile";
while( $line = <FILE> ) {
    chomp $line; if( $line eq "" || substr( $line, 0, 1 ) eq "#" ) { next; }
    @_ = split " ", $line;
    if( uc( $_[ 0 ] ) eq "RESOURCE" && ( $#_ == 1 || $#_ == 2 ) ) {

	!defined( $resources{ $_[ 1 ] } )
	    or die "ERROR: resource $_[1] multiply defined";
	if( $#_ == 2 ) {
	    $resources{ $_[ 1 ] } = $_[ 2 ];
	} else {
	    $resources{ $_[ 1 ] } = 1;
	}
    } else {
	$#_ >= 3 or die "ERROR: machine must be 'ID PLAYER MACHINE EXECUTABLE [RESOURCE ...]': $line";
	$machine = shift @_;
	!defined( $machines{ $machine } )
	    or die "ERROR: machine $machine multiply defined";
	$p = $_[ 0 ];
	defined( $players{ $p } ) or die "ERROR: unknown player $p in $line";
	for( $i = 3; $i <= $#_; ++$i ) {
	    defined( $resources{ $_[ $i ] } )
		or die "ERROR: unknown resource $_[$i] in $line";
	}
	$machines{ $machine } = [ @_ ];
	push @{$players{ $p }}, $machine;
    }
}
close FILE;

open FILE, "<", $matchFile
    or die "ERROR: could not open match file $matchFile";
while( $line = <FILE> ) {
    chomp $line; if( $line eq "" || substr( $line, 0, 1 ) eq "#" ) { next; }
    @_ = split " ", $line;
    $#_ >= 4 or die "ERROR: 0 players listed in match $line";
    $m = shift @_;
    $m = uc( $m );
    !defined( $matches{ $m } ) or die "ERROR: match $m multiply defined";
    for( $i = 3; $i <= $#_; ++$i ) {
	defined( $players{ $_[ $i ] } )
		 or die "ERROR: unkwnown player $_[ $i ] in $matchFile";
    }
    $matches{ $m } = [ @_ ];
}
close FILE;

if( open FILE, "<", $transFile ) {
    while( $line = <FILE> ) {
	chomp $line;
	if( $line eq "" || substr( $line, 0, 1 ) eq "#" ) { next; }
	@_ = split " ", $line;
	$#_ >= 1 or die "ERROR: transaction should be MATCH STATUS ...: $line";
	$m = shift @_;
	if( !defined( $matches{ $m } ) ) {
	    # transaction on a match that has since been removed?
	    next;
	}
	$matchStatus{ $m } = [ @_ ];
    }
    close FILE;
}

open FILE, ">>", $transFile
    or die "ERROR: could not open transaction file $transFile for writing";

# take action based on transaction status
$running = 0;
foreach $m ( keys %matches ) {
    if( !defined( $matchStatus{ $m } ) ) {
	# match hasn't been started yet - deal with this later
	next;
    }

    $s = ${$matchStatus{ $m }}[ 0 ];

    if( $s eq "FINISHED" ) {
	# match finished: remove it from match list

	delete $matches{ $m };
    } elsif ( $s eq "RUNNING" ) {
	# match running: query the server for updated status
	
	$queryResult = queryStatus( $m );
	if( $queryResult eq "NONE" ) {
	    # uh-oh!  we've run something, but server doesn't have it!

	    print "ERROR: match $m started, but is missing from server\n";
	    print FILE "$m ERROR\n";
	    delete $matches{ $m };
	} elsif( $queryResult eq "RUNNING" ) {
	    # still running: remove match, and resources used

	    $#{$matchStatus{ $m } } - 1 == $#{$matches{ $m }} - 3
		or die "ERROR: wrong # of bots for $m RUN transaction";
	    for( $i = 1; $i <= $#{$matchStatus{ $m } }; ++$i ) {
		$machine = ${$matchStatus{ $m }}[ $i ];

		defined( $machines{ $machine } )
		    or die "ERROR: unknown machine $machine for $m RUN transaction";
		modifyMachineResources( $machine, -1 );
		delete $machines{ $machine };
	    }
	    delete $matches{ $m };
	    ++$running;
	} elsif( $queryResult eq "FINISHED" ) {
	    # match finished: remove it from match list

	    print FILE "$m FINISHED\n";
	    delete $matches{ $m };
	} elsif( $queryResult eq "ERROR" ) {
	    # error occurred on server side while running match

	    print "ERROR: problem running match $m\n";
	    print FILE "$m ERROR\n";
	    delete $matches{ $m };
	}
    } elsif ( $s eq "ERROR" ) {
	# match finished with an error: remove it from match list and complain

	print "$m failed with an ERROR\n";
	delete $matches{ $m };
    } else {

	die "ERROR: unknown transaction status $i for $m";
    }
}

# go through all remaining matches, trying to run them
MATCH: foreach $m ( keys %matches ) {
    $matchRef = $matches{ $m };


    # remove any machines that we know are missing resources
    foreach $machine ( keys %machines ) {
	if( !checkMachineResources( $machine ) ) {
	    delete $machines{ $machine };
	}
    }

    # try scheduling the match
    @matchMachines = scheduleMatch( $m, 0 );
    if( $#matchMachines < 0 ) {
	for( $p = 3; $p <= $#$matchRef; ++$p ) {
	    ++$unfinishedPlayers{ $$matchRef[ $p ] };
	}
	next MATCH;
    }

    # found a machine for each player
    $i = "$m $$matchRef[ 0 ] $$matchRef[ 1 ] $$matchRef[ 2 ]";
    $t = "$m RUNNING";
    for( $p = 3; $p <= $#$matchRef; ++$p ) {
	$machine = $matchMachines[ $p - 3 ];
	$machinesRef = $machines{ $machine };

	# 1 is the buy-in, overwritten by server gamedef, must be positive?
	$i .= " AAAIPLAYER $$matchRef[ $p ] 1 $$machinesRef[ 1 ] $$machinesRef[ 2 ]";
	$t .= " $matchMachines[ $p - 3 ]";
	modifyMachineResources( $machine, -1 );
	delete $machines{ $machine };
    }
    print "running $i\n";
    `$matchProg $i`;
    ( $? >> 8 ) == 0
	or die "ERROR: could not create match";
    print FILE "$t\n";
    ++$running;
}

# find any machines that we can free up
foreach $machine ( keys %machines ) {
    $p = ${$machines{ $machine } }[ 0 ];

    if( $unfinishedPlayers{ $p } > 0 ) {
	--$unfinishedPlayers{ $p };
    } else {
	print "finished with player resource $machine\n";
    }
}

if( $running == 0 ) {
    print "FINISHED ALL MATCHES\n";
}

# POD Documentation for usage message
__END__

=head1 NAME

B<ACPCScheduleMatches> - Automated tool for starting matches using the
GlassFrog server

=head1 SYNOPSIS

B<ACPCScheduleMatches.pl> [options] serverMachine playerFile resourceFile
matchFile transactionFile

=head1 DESCRIPTION

B<ACPCScheduleMatches> takes several files as arguments which specify that
matches to be run and where different resources can be found.  The
B<transactionFile> will record the state of a match (i.e., if it was started,
if it has finished, or if it ran into an error).  This tool is designed to help
automate the creation of large tournaments as opposed to small one-off
experiments.  For individual experiments, it may be easier to just use
matchConstructor.py.

The required arguments are:

=over 8

=item B<serverMachine>

The IP address of the GlassFrog server that will be running the matches.
C<localhost> can be used if the server is running locally.

=item B<playerFile>

A file with a list of player names.  One player name per line.

If you used ACPCMatchCreator.pl to generate the B<matchFile>, then playerFile
will be the same here as what was used with ACPCMatchCreator.pl.

=item B<resourceFile>

A file containing a list of machine resources where players can be found.

This file contains both resource and player instances information.  A
resource line specifies a consumable resource, with an optional count.

Instances of players should have at least four entries on each line
separated by spaces.  The first entry is the instance tag (an
arbitrary name you assign).  The second entry is the player name
(which should contained in B<playerFile>).  Third is the IP address of
the machine where the resource lives (LOCAL can be used for the local
machine).  Fourth is the name of the program to start the
resource/bot.  Any additional items are all (previously defined)
resources which the instance requires to run.

For example,

 RESOURCE machine1
 RESOURCE machine2 2
 a1 a machine1.cs.ualberta.ca scripts/randomChump.py machine1
 a2 a machine2.cs.ualberta.ca scripts/randomChump.py machine2
 b1 b machine1.cs.ualberta.ca scripts/randomChump.py machine1
 b2 b machine2.cs.ualberta.ca scripts/randomChump.py machine2
 c1 c machine1.cs.ualberta.ca scripts/randomChump.py machine1
 c2 c machine2.cs.ualberta.ca scripts/randomChump.py machine2

lists a setup where there are two instances of both players a, b and
c.  machine1 can only handle running one player at a time, but
machine2 can handle two players running at the same time.

=item B<matchFile>

A file containing a list of matches that you want to run.  

This file could simply be the output of ACPCMatchCreator.pl using the
parameters for your desired matches (or a similar match listing which could be
produced by hand).

=item B<transactionFile>

A file containing match transaction records.  If this file doesn't already
exist, it will be created.  Otherwise it will be appended to.  Note that this
file can be edited by hand if desired.

The B<transactionFile> will record the state of a match (i.e., if it was
started, if it has finished, or if it ran into an error).

=back

=head1 OPTIONS

=over 8

=item B<--help>

Print a brief help message and exits.

=item B<--man>

Prints the manual page and exits.

=back

=head1 EXAMPLES

Let F<PlayerList> be:

 a
 b

Let F<ResourceList> consist of two resources: 

 a1 a LOCAL scripts/randomChump.py
 b1 b LOCAL scripts/randomChump.py
 
Let F<MatchList> be a file containing the output of ACPCMatchCreator.pl using
the parameters for your desired matches (for this example we are using the
output from the example presented in the ACPCMatchCreator manual).

Then, assuming GlassFrog is running, ACPCScheduleMatches can be run in a loop
with all of these files, along with a transaction file.  If we have GlassFrog
running on localhost then (for bash) we can run:

while true; do tools/ACPCScheduleMatches.pl localhost PlayerList ResourceList
MatchList TransactionFile; sleep 10; done

If everything is set up right, it will immediately print something like:

running TEST_MATCH_APR29_1004.2 100 2Player.limit.gamedef.xml 342387623
AAAIPLAYER b 1 LOCAL scripts/randomChump.py AAAIPLAYER a 1 LOCAL
scripts/randomChump.py

and then sleep for 10 seconds.  Once the first match is finished and the sleep
finishes, the next instance of ScheduleMatches will print another "running"
line as it starts the second match.  After that finishes, it will print out

 finished with player resource b1
 finished with player resource a1

to let you know that there are no longer enough matches to require resource b1.
If there are multiple instances for a single player, it will note that some of
them are no longer needed as soon as there are too few matches left for that
player.   You can edit the resource file and remove the resoure at that point
if you don't want to see the message any more.  This is also the point at which
you could decide to use those same hardware resources to host another player.

If anything fails, it'll print out an ERROR line once, and then a slightly
different error message forever afterwards.  The match failure will also
be in the transaction log.  There's a couple of things you could do.  You
could try fixing the players and then just remove the match start and error
from the transaction file.  It will then try to resume the match in GlassFrog.  If you want to cut the match short and re-try completely, remove the match
from the match file instead and add a new one.  For example, take out

test_match_Apr29_1004.1 100 2Player.limit.gamedef.xml 342387623 a b

and add

retry1.test_match_Apr29_1004.1 100 2Player.limit.gamedef.xml 342387623 a b

=cut
