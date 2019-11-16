#include "properties.prp"

/**
 * This is a model for a three player distributed rock-paper-scissors game.
 * There are three players and a referee who decides the winner. The players
 * must send their choise of rock, paper, and scissors to the referee during
 * some time interval. If a player fails to do so, then the player is taken to
 * wait_for a timeout option. Timeout always loses.
 */
mtype = {ROCK, PAPER, SCISSORS, TIMEOUT};

/**
 * There are three possible outcomes for a single round for each player. A
 * player wins, if the other two players lose. Two or three players end up in
 * TIE if they all play either rock, paper, or scissors. A player looses on
 * timeout or traditionally. Traditionally, paper beats rock, rock beats
 * scissors, and scissors beat paper.
 */
mtype = {WIN, TIE, LOSE};

/**
 * A total of five rounds will be played, after which the referee declares the
 * winner of the game. There is either exactly one winner, or otherwise the
 * game ends inconclusively.
 */
mtype = {P1WIN, P2WIN, P3WIN, INCONCLUSIVE};

bool play[3];   /* Used by referee for signaling players when to play. */

mtype players[3]; /* A global array representing the plays of the players. */
mtype results[3]; /* A global array representing the latest results. */

mtype outcome; /* The final outcome of the game. */

/* The following three helper variables are only used for verifying the LTL
   property "conclusiveness": */
byte rocks;    /* Number of rocks played in a round.    */
byte papers;   /* Number of papers played in a round.   */
byte scissors; /* Number of scissors played in a round. */

/**
 * Compares the plays of two players. pa and pb represent the plays of the
 * players while ca and cb count the number of wins of the players a and b in
 * this round. The counter for a winning player is incremented.
 */
inline compare(pa, pb, ca, cb)
{
    if
    ::  pa - pb != 0 ->
            if
            ::  pa == ROCK     && pb == PAPER    -> cb++
            ::  pa == ROCK     && pb == SCISSORS -> ca++
            ::  pa == PAPER    && pb == ROCK     -> ca++
            ::  pa == PAPER    && pb == SCISSORS -> cb++
            ::  pa == SCISSORS && pb == ROCK     -> cb++
            ::  pa == SCISSORS && pb == PAPER    -> ca++
            ::  pa == TIMEOUT  && pb == TIMEOUT  -> skip
            ::  pa == TIMEOUT  && pb != TIMEOUT  -> cb++
            ::  pa != TIMEOUT  && pb == TIMEOUT  -> ca++
            fi
    ::  else -> skip
    fi
}

/**
 * Decides the results based on points. c1, c2, and 3 represents the points of
 * players 1, 2, and 3 respectively.
 */
inline judge(c1, c2, c3, r1, r2, r3)
{
    if
    ::  c1 == c2 && c2 == c3 -> 
        if
        ::  c1 == 0 && players[0] != TIMEOUT -> r1 = TIE; r2 = TIE; r3 = TIE
        ::  else -> 
                /* Either the round ended in cyclic play (e.g. any permutation
                of ROCK - PAPER - SCISSORS, or all players timed out. In these
                situations, giving points or calling it a tie doesn't make
                sense.*/
                r1 = INCONCLUSIVE;
                r2 = INCONCLUSIVE;
                r3 = INCONCLUSIVE;
                c1 = 0;
                c2 = 0;
                c3 = 0;
        fi
    ::  c1 > c2  && c2 >= c3 -> r1 = WIN;  r2 = LOSE; r3 = LOSE
    ::  c1 > c3  && c3 >= c2 -> r1 = WIN;  r2 = LOSE; r3 = LOSE
    ::  c2 > c1  && c1 >= c3 -> r1 = LOSE; r2 = WIN;  r3 = LOSE
    ::  c2 > c3  && c3 >= c1 -> r1 = LOSE; r2 = WIN;  r3 = LOSE
    ::  c3 > c1  && c1 >= c2 -> r1 = LOSE; r2 = LOSE; r3 = WIN
    ::  c3 > c2  && c2 >= c1 -> r1 = LOSE; r2 = LOSE; r3 = WIN
    ::  c1 == c2 && c2 > c3  -> r1 = TIE;  r2 = TIE;  r3 = LOSE
    ::  c1 == c3 && c3 > c2  -> r1 = TIE;  r2 = LOSE; r3 = TIE
    ::  c2 == c3 && c3 > c1  -> r1 = LOSE; r2 = TIE;  r3 = TIE
    fi
}

/**
 * Decides the outcome based on results for players 1, 2, and 3.
 */
inline decideOutcome(r1, r2, r3, outcome)
{
    if
    ::  r1 == WIN -> outcome = P1WIN
    ::  r2 == WIN -> outcome = P2WIN
    ::  r3 == WIN -> outcome = P3WIN
    ::  else      -> skip
    fi
}

/**
 * This process type represents a player as a standalone client in the
 * distributed system for the rock-paper-scissors game. Players remain passive
 * until the referee asks them to play by setting their respective play value
 * to true. After playing or timing out, the play value is set to false again.
 */
proctype Player(byte i)
{
    /* A label prefixed with "end" tells Spin that this is a valid end state for
       the process: */
    end_player: do
    ::  play[i] -> 
        if
        ::  players[i] = ROCK;     rocks++     /* Player i chose rock. */
        ::  players[i] = PAPER;    papers++    /* Player i chose paper. */
        ::  players[i] = SCISSORS; scissors++  /* Player i chose scissors. */
        ::  players[i] = TIMEOUT               /* Player i timed out. */
        fi
        play[i] = false
    od
}

/**
 * The Referee process type represents the process responsible for deciding the
 * outcome of the three-player rock-paper-scissors game. The players 
 */
proctype Referee()
{
    outcome = INCONCLUSIVE;
    byte i  = 1; /* Number of the round.                   */
    byte c1 = 0; /* Total number of wins for player 1.     */
    byte c2 = 0; /* Total number of wins for player 2.     */
    byte c3 = 0; /* Total number of wins for player 3.     */
    byte d1;     /* Number of wins for player 1 per round. */
    byte d2;     /* Number of wins for player 2 per round. */
    byte d3;     /* Number of wins for player 3 per round. */
    do
    ::  i < 6 -> roundStarts: printf("Round %d:\n", i);
                 d_step /* Synchronisation barrier */
                 {
                     rocks    = 0;
                     papers   = 0;
                     scissors = 0;
                     play[0]  = true;
                     play[1]  = true;
                     play[2]  = true;
                 }

                 /* Block until every player has played or timed out: */
                 atomic
                 {
                     !play[0] && !play[1] && !play[2];
                 }
                 d_step
                 {
                     printf("        Player 1 chose %e.\n", players[0]);
                     printf("        Player 2 chose %e.\n", players[1]);
                     printf("        Player 3 chose %e.\n", players[2]);
                     d1 = 0;
                     d2 = 0;
                     d3 = 0;
                     compare(players[0], players[1], d1, d2);
                     compare(players[0], players[2], d1, d3);
                     compare(players[1], players[2], d2, d3);
                     judge(d1, d2, d3, results[0], results[1], results[2]);
                     printf("    Results:\n");
                     printf("        Player 1: %e (%d points)\n", results[0], d1);
                     printf("        Player 2: %e (%d points)\n", results[1], d2);
                     printf("        Player 3: %e (%d points)\n", results[2], d3);
                     c1 = c1 + d1;
                     c2 = c2 + d2;
                     c3 = c3 + d3;
                 }
                 roundEnds: i = i + 1
    ::  i >= 6 -> break
    od
    atomic
    {
        judge(c1, c2, c3, results[0], results[1], results[2]);
        decideOutcome(results[0], results[1], results[2], outcome);
    }
    gameEnds: printf("Final Results:\n");
    printf("    Player 1: %d points\n", c1);
    printf("    Player 2: %d points\n", c2);
    printf("    Player 3: %d points\n", c3);
    if
    ::  outcome == P1WIN        -> printf("Player 1 wins.\n")
    ::  outcome == P2WIN        -> printf("Player 2 wins.\n")
    ::  outcome == P3WIN        -> printf("Player 3 wins.\n")
    ::  outcome == INCONCLUSIVE -> printf("The game ends in a tie.\n")
    fi
}

init
{
    run Player(0); /* Player 1. */
    run Player(1); /* Player 2. */
    run Player(2); /* Player 3. */
    run Referee();
}
