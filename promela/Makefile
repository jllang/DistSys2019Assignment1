separator = ================================================================================

build:
	spin -a model.pml                                                    && \
	gcc -o pan pan.c                                                     && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N everyRoundEndsEventually -w26                         && \
#	echo "\n$(separator)\n"                                              && \
#	./pan -a -n -N atLeastOneWinnerPerRound                              && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N atMostOneWinnerPerRound                               && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N atMostOneWinnerOverall                                && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N playerOneNeverWins                                    && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N playerTwoNeverWins                                    && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N playerThreeNeverWins                                  && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N samePlayMeansSameResult                                && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N conclusiveness                                        && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N p1p2classical                                         && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N p1p3classical                                         && \
	echo "\n$(separator)\n"                                              && \
	./pan -a -n -N p2p3classical
