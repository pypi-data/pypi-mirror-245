Name                      iterations sum        mean       median     p95        p99
Python                    100        0.304ms    0.003ms    0.002ms    0.007ms    0.024ms
Python                    1000       2.026ms    0.002ms    0.002ms    0.002ms    0.003ms
Python                    10000      22.321ms   0.002ms    0.002ms    0.003ms    0.004ms

Aioinject                 100        1.993ms    0.020ms    0.014ms    0.037ms    0.285ms
Aioinject                 1000       13.404ms   0.013ms    0.012ms    0.021ms    0.032ms
Aioinject                 10000      130.890ms  0.013ms    0.012ms    0.019ms    0.030ms

Aioinject - Decorator     100        1.442ms    0.014ms    0.013ms    0.023ms    0.035ms
Aioinject - Decorator     1000       14.429ms   0.014ms    0.013ms    0.022ms    0.039ms
Aioinject - Decorator     10000      138.885ms  0.014ms    0.013ms    0.018ms    0.029ms

FastAPI - /depends        100        84.963ms   0.850ms    0.810ms    1.027ms    4.177ms
FastAPI - /depends        1000       806.565ms  0.807ms    0.768ms    0.953ms    1.019ms
FastAPI - /depends        10000      7852.714ms 0.785ms    0.765ms    0.947ms    1.032ms

FastAPI - /aioinject      100        31.446ms   0.314ms    0.271ms    0.428ms    2.763ms
FastAPI - /aioinject      1000       319.066ms  0.319ms    0.276ms    0.410ms    0.505ms
FastAPI - /aioinject      10000      3000.845ms 0.300ms    0.274ms    0.405ms    0.480ms

FastAPI - /by-hand        100        26.836ms   0.268ms    0.247ms    0.372ms    0.534ms
FastAPI - /by-hand        1000       277.470ms  0.277ms    0.253ms    0.376ms    0.438ms
FastAPI - /by-hand        10000      2768.416ms 0.277ms    0.252ms    0.375ms    0.445ms

Strawberry - by_hand      100        56.042ms   0.560ms    0.546ms    0.682ms    1.119ms
Strawberry - aioinject    100        56.448ms   0.564ms    0.569ms    0.676ms    0.727ms
Strawberry - by_hand      1000       552.270ms  0.552ms    0.551ms    0.690ms    0.767ms
Strawberry - aioinject    1000       589.598ms  0.590ms    0.572ms    0.708ms    0.784ms
Strawberry - by_hand      10000      5547.539ms 0.555ms    0.549ms    0.680ms    0.753ms
Strawberry - aioinject    10000      5856.649ms 0.586ms    0.579ms    0.715ms    0.794ms   
