/*
Implementation of the Box-Muller transform
*/
function box_muller(mu, sigma) {
    var x, y, r, v = 0;
    do {
        x = 2 * Math.random() - 1;
        y = 2 * Math.random() - 1;
        r = x * x + y * y;
    }
    while (r >= 1);
    co = Math.sqrt(-2 * Math.log(r) / r);
    v = x * co;
    return v * sigma + mu;
}

/*
Generate an exponential distribution using inverse CDF
*/
function generate_exp(lambda) {
    var ex, u = 0;
    u = Math.random();
    ex = -(1 / lambda) * Math.log(1 - u);
    return ex;
}

/*
Generate a logistic distribution using inverse CDF
*/
function generate_logistic(mu, sigma) {
    var lgstc, u = 0;
    u = Math.random();
    lgstc = mu + sigma * Math.log(u / (1 - u));
    return lgstc;
}