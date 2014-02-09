#!/usr/bin/perl

use strict vars;

use Getopt::Long;
use Pod::Usage;

my( @players, $game, $numPlayersInGame, $hands, $baseMatchName,
     $numMatchPermutations, @seeds );
my( $matches );


# arguments: n
# returns: n!
sub factorial
{
    my( $f, $i );

    $f = 1;
    for( $i = 2; $i <= $_[ 0 ]; ++$i ) {
	$f *= $i;
    }

    return $f;
}

# arguments: rank numObjects
# returns: @permutation
sub unRankPermutation
{
    my( $rank, $numObjects ); $rank = $_[ 0 ]; $numObjects = $_[ 1 ];
    my( $i, $end, $t, @loc, @perm );

    $i = $numObjects - 1;
    $end = 0;
    $loc[ $end ] = $i;
    $perm[ $i ] = $end;

    while( $i > 0 ) {
	--$i;
	++$end;

	$t = $rank % ( $numObjects - $i );
	$rank /= $numObjects - $i;

	if( $t == $end ) {
	    $loc[ $end ] = $i;
	    $perm[ $i ] = $end;
	} else {
	    $loc[ $end ] = $loc[ $t ];
	    $loc[ $t ] = $i;
	    $perm[ $loc[ $end ] ] = $end;
	    $perm[ $i ] = $t;
	}
    }

    return @perm;
}

# arguments: \botsInMatchup
sub permuteBots
{
    my( $botsRef ); $botsRef = $_[ 0 ];
    my( @permutations, $numPermutations, $permRank, $s, $i, @perm );

    # choose the required number of random permutations
    $numPermutations = factorial( $numPlayersInGame );
    while( $#permutations + 1 < $numMatchPermutations ) {

	# skip any permutations we have already tried
	$permRank = int( rand() * $numPermutations );
	for( $i = 0; $i <= $#permutations; ++$i ) {
	    if( $permutations[ $i ] == $permRank ) {
		last;
	    }
	}
	if( $i <= $#permutations ) {
	    # have already seen this permutation
	    next;
	}

	# add to list of used permutations
	push @permutations, $permRank;

	# unpack the chosen permutation
	@perm = unRankPermutation( $permRank, $numPlayersInGame );
	for( $s = 0; $s <= $#seeds; ++$s ) {
	    print "$baseMatchName.$matches $hands $game $seeds[ $s ]";
	    for( $i = 0; $i < $numPlayersInGame; ++$i ) {
		print " $players[ $$botsRef[ $perm[ $i ] ] ]";
	    }
	    print "\n";
	    ++$matches;
	}
    }
}

# arguments: \@bots
sub chooseBots
{
    my( $botsRef ); $botsRef = $_[ 0 ];
    my( $i, $start );

    if( $#{$botsRef} + 1 >= $numPlayersInGame ) {
	permuteBots( $botsRef );
	return;
    }

    if( $#{$botsRef} < 0 ) {
	$start = 0;
    } else {
	$start = $$botsRef[ $#{$botsRef} ] + 1;
    }
    for( $i = $start; $i <= $#players; ++$i ) {
	push @$botsRef, $i;
	chooseBots( $botsRef, $numPlayersInGame );
	pop @$botsRef;
    }
}


my( $usage, $man, $help, $s, $line, $playerFile, $permSeed );

GetOptions( 'help' => \$help, 'man' => \$man ) 
  or pod2usage( -exitstatus => 2, 
                -message => "Invalid arguments.\n" .
                            "Use --help or --man for detailed usage.");
pod2usage( -verbose => 1 ) if( $help );
pod2usage( -verbose => 2 ) if( $man );
$#ARGV >= 7
  or pod2usage( -exitstatus => 2, 
                -message => "Insufficient arguments.\n" .
                            "Use --help or --man for detailed usage.");

$hands = $ARGV[ 0 ];
$game = $ARGV[ 1 ];
$numPlayersInGame = $ARGV[ 2 ];
$playerFile = $ARGV[ 3 ];
$numMatchPermutations = $ARGV[ 4 ];
if( $numMatchPermutations <= 0 ) {
    $numMatchPermutations = factorial( $numPlayersInGame );
} else {
    $numMatchPermutations <= factorial( $numPlayersInGame )
	or die "$numMatchPermutations is too many match permutations for a $numPlayersInGame player game";
}
$permSeed = $ARGV[ 5 ];
$baseMatchName = $ARGV[ 6 ];
for( $s = 7; $s <= $#ARGV; ++$s ) {
    push @seeds, $ARGV[ $s ];
}

# print out arguments, so we can re-construct events
$usage = "numHandsPerMatch game numPlayersInGame playerFile numMatchPermutations permutationSeed baseMatchName handSeed1 [handSeed2 ...]";
print "# $usage\n";
print "#";
for( $s = 0; $s <= $#ARGV; ++$s ) {
    print " $ARGV[ $s ]";
}
print "\n";

srand( $permSeed );

open FILE, "<", $playerFile or die "could not open player file $playerFile";
while( $line = <FILE> ) {
    chomp $line; if( $line eq "" || substr( $line, 0, 1 ) eq "#" ) { next; }
    @_ = split " ", $line;
    push @players, $_[ 0 ];
}
close FILE;

$matches = 1;
chooseBots( [] );


# POD Documentation for usage message
__END__

=head1 NAME

B<ACPCMatchCreator> - Outputs a tournament match list from tournament parameters

=head1 SYNOPSIS

B<ACPCMatchCreator.pl> [options] numHandsPerMatch game numPlayersInGame
playerFile numMatchPermutations permutationSeed baseMatchName handSeed1
[handSeed2 ...]

=head1 DESCRIPTION

B<ACPCMatchCreator> takes several parameters for the tournament that you want
to create and outputs a match list to standard output.  This tool isn't
required for creating matches: they can also be made by hand using
matchConstructor.py.  This tool is designed to help automate the creation of
large tournaments as opposed to small experiments.  Note that although
ACPCMatchCreator outputs script generated match information, the resulting
output can be edited by hand if you desire.

The required arguments are:

=over 8

=item B<numHandsPerMatch>

The integer number of hands in each of the tournament matches.

=item B<game>

The name of the XML gamedef file for the game used in the matches (e.g.,
F<2Player.limit.gamedef.xml>).

=item B<numPlayersInGame>

The number of players in the specified game.

=item B<playerFile>

A file with a list of player names.  One player name per line.

=item B<numMatchPermutations>

The number of match permutations to use.  For instance, to generate full
duplicate matches in an N player game, this number should be all permutations
of the N players' seating arrangement (i.e., N!).  If you want all
permutations, specify a value <=0.  Using less than all possible permutations
will result in random sampling of the possible seating arrangements.

=item B<permutationSeed>

The random number seed used for sampling the player seating arrangements. 

=item B<baseMatchName>

The base name for each of the matches that will be generated.  Note that match
names are converted to upper case by GlassFrog so do not rely on capitalisation
to distinguish matches.

=item B<handSeed1>

Random number seed for the dealer to control the hands dealt to players.  You
may provide an arbitrary number of hand seeds (though at least one is
required).  Each seed will produce a separate match for the cards generated by
the given seed.

=back

=head1 OPTIONS

=over 8

=item B<--help>

Print a brief help message and exits.

=item B<--man>

Prints the manual page and exits.

=back

=head1 EXAMPLES

Let F<PlayerList> be a player file for agents C<a> and C<b>.  This would simply be:

 a
 b

Lets say I wanted to set up a round-robin competition with 100 hand matches of
the 2Player.limit.gamedef.xml game, which I know has 2 players.  I've already
got my list of players.  For each pairing of players, I want to do all
permutations, which I can specify by using a value <=0.  It's sampling the
permutations randomly, so I need to give it a random number seed, like
13064987132.  I'm doing test matches on April 29 at 10:04, so I'm choosing
match names of the form test_match_Apr29_1004.  Every match needs a random seed
for the dealer to control the hands dealt.  I'm going to use 342387623.  Given
all of this, I run

tools/ACPCMatchCreator.pl 100 2Player.limit.gamedef.xml 2 PlayerList 0
13064987132 TEST_MATCH_APR29_1004 342387623

It just spews to standard output.  I verify that it's doing what I want,
then capture the output.  I stick it in MatchList

tools/ACPCMatchCreator.pl 100 2Player.limit.gamedef.xml 2 PlayerList 0
13064987132 TEST_MATCH_APR29_1004 342387623 > MatchList

If I wanted to do 5 out the 6 seating permutations in a 3 player game, and I
wanted to use 3 different sets of hand seeds for the dealer, I could do

tools/ACPCMatchCreator.pl 100 3Player.limit.gamedef.xml 3 PlayerList 5
13064987132 TEST_MATCH_3P_APR29_1004 342387623 608453641 3361947158

This would end up creating 15 matches for every set of three players.

=cut
