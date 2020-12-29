- optimal vector $w \in \{0,1\}^P$, where dimension $P$ is the number of players
- first $m$ are qbs, next $n$ are wr....
  - 1 means selected player
- points total $F = w^T\delta$
- opponent point totals $G_o = w_o^T\delta$
  - so then $\delta$ is the vector of player performances

### Constraints

- must select $C$ (chosen) players (perhaps 9)
- total cost must not be more than budget $B$
- $W$ is the set of binary vectors $w$ satisfying these constraints

- also want to have $c^Tw_o >= B_{lb}$ for some lower bound $B_{lb} <= B$, because a player is very likely to use most of their available budget

> There may be other constraints imposed by Fanduel

- modelled as linear constraints

### Problem Formulation

- we want to maximize the expected value of our collection of entries into the competition
  - we optimize on the expected value of our portfolio in such a way that we maximize the $probability * value$ of being in the money for each of our entries (see equation in section 2.2)

### Modelling Opponents Selections

- we do not have access to opponent selections prior to the contest, so we must model them
- we can do this using **Dirichlet Regression**
  - for example, we have $N_{QB}$ quarterbacks with $P_{QB} \sim Dir(\alpha_{QB})$
  - $P_{QB}$ is a vector of probabilities of length $N_{QB}$, where QB _k_ is selected with probability $p_{QB}^k$ for $k = 1, ..., N_{QB}$

#### Independent variables needed for Dirichlet Regression

- $f_{QB}$ estimate of $P\_{QB}
- $c_{QB}$ cost for each quarterback
- $\mu_{QB}$ expected player performance

- $P_{QB }^t$ for days $t = 1$ to $t = T-1$

  > One potential wrinkle here is that NBA teams don't play every day - will it make a difference if there are entries with 0 probability?

- with these variables we can do a Dirichlet regression, perhaps using the **Bayesian software package STAN** (interface available for R and Python)
- with results of Dirichlet regression we can draw samples from Multinomial distribution generated using the probabilities determined by the Dirichlet regression (I don't understand this part)

  > We can try and implement stacking behaviour as they do in one of the numerical experiments

- Then we run an algorithm that samples $O$ opponent portfolios (expected number of contest entries - our entries), accepting $w_o$ if it satisfies the constraints, and rejecting it otherwise, looping until we have generated all $O$ portfolios.

#### Useful Links

> in the paper they got projected points and ownership from Fantasypros, but for NBA it looks like they don't have ownership, and you have to pay for points.

- projected ownership: (https://www.linestarapp.com/Ownership/Sport/NBA/Site/FanDuel)
- projected points and ownership: (https://www.rotowire.com/daily/nba/optimizer.php?site=FanDuel)
- projected points: (https://www.dailyfantasyfuel.com/nba/projections/fanduel)
  - this one is good because you can download csv

### Solving the Double-up problem

- we use some proof I don't understand in order to solve a linear program that maximizes $\mu_w$ over $w \in W$

  - then we use the result to determine which case of the proof we are in
  - we form a grid $\Lambda$ of possible $\lambda$ values, solving a quadratic optimization, and choose the value of $\lambda$ that yields the largest objective depending in the case of the proof we are in.

- we figure out the mean and variance of $G(r')$, which is the $r'^{th}$ order statistic (the point total of the entry just outside the money)

  - it says we can figure these out by doing a Monte-Carlo simulation

- we can use **Gurobi's default binary quadratic program solver** for each $\lambda$ in $\Lambda$
- $\lambda^*$ can be computed using the monte-carlo samples of $\delta$ and $w_o$ that are inputs into the algoritm, or by using the normal approximation assumption (?)
- the algorithm returns the optimal vector of players, $w_{\lambda^*}$.

### Solving Top-heavy problem

- we are in case 1 of the proof. Solve BQP's and get $\lambda^*$ from monte-carlo samples.

#### Multiple entries

- we can use a greedy approach, imposing constraints that diversify our portfolio of entries.
  - they found that diversification was more profitable than replication.
- solve for the optimal $N = 1$ entry. Then for $i = 2, ..., N$, solve for the optimal entry, with the additional constraint that the new portfolio cannot have more than $\gamma$ players in common with the previous entries
- we can figure out the optimal value of $N$ by doing monte-carlo samples in order to estimate profit & loss of a portfolio of entries, continuing to increment $N$ until the expected P&L from the next contribution goes negative

### Questions for Steve

- Dirichlet -> Multinomial
- Copula
- How do we do the optimization?
