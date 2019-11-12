separator = ================================================================================

build:
	spin -a model.pml                                                    && \
	gcc -o pan pan.c                                                     && \
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
	./pan -a -n -N conclusiveness
