import numpy
import csv

chances = numpy.array([114,113,112,111,99,89,79,69,59,49,39,29,19,9,6,4])
weights = chances/float(sum(chances))
odds = numpy.zeros((weights.size,weights.size))

# loop through to create all of the possible permutations of pick order without any duplicates
for i,wi in enumerate(weights):
    for j,wj in enumerate(weights):
        if (j not in [i]):
            for k,wk in enumerate(weights):
                if (k not in [i,j]):
                    for l,wl in enumerate(weights):
                        if (l not in [i,j,k]):
                            for m,wm in enumerate(weights):
                                if (m not in [i,j,k,l]):
                                    for n,wn in enumerate(weights):
                                        if (n not in [i,j,k,l,m]):
                                            # calculate all of the conditional probabilities, adjusting the weights after each pick
                                            odds[i,0] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
                                            odds[j,1] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
                                            odds[k,2] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
                                            odds[l,3] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
                                            odds[m,4] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
                                            odds[n,5] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
                                            for p,wp in enumerate(weights):
                                                # Here we need to quantify how many lower seeds went ahead of the current one
                                                if (p not in [i,j,k,l,m,n]):
                                                    a = numpy.array([i,j,k,l,m,n])
                                                    shift = (a > p).sum()
                                                    odds[p,p+shift] += wi * wj/(1-wi) * wk/(1-(wi+wj)) * wl/(1-(wi+wj+wk)) * wm/(1-(wi+wj+wk+wl)) * wn/(1-(wi+wj+wk+wl+wm))
# write the results out to a CSV
odds_data = open('odds.csv', 'wb')
csvwriter = csv.writer(odds_data)
for i in range(len(odds)):
    csvwriter.writerow(odds[i])
odds_data.close()