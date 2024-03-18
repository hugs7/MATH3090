# MATH3090 Assignment 1

Student: Hugo Burton (s4698512)
Date Due: Tuesday March 19 @ 1pm


```python
import math
from typing import Dict
from colorama import Fore, Style
import numpy as np
from IPython.display import Markdown, display

import bond
import interest
import newtons
import display as dsp
```

## Question 1 (6 marks)

### Part A (3 marks)


Suppose a company issues a zero coupon bond with face value $10,000 and which matures in 20 years. Calculate the price given:


```python
face_value = 10_000
years_to_maturity = 20
```

i. An 8\% discount compound annual yield, compounded annually.


```python
# Question i
interest_rate = 0.08
compounding_frequency_yr = 1

price_i = bond.price_zero_coupon_bond_discrete(
    face_value, years_to_maturity, interest_rate, compounding_frequency_yr)

dsp.display_answer(price_i)
```

    [32mAnswer:[0m $2145.48
    

ii. An 8\% discount continuous annual yield, compounded semi-annually.


```python
# Question ii
interest_rate = 0.08

price_ii = bond.price_zero_coupon_bond_continuous(
    face_value, years_to_maturity, interest_rate)

dsp.display_answer(price_ii)
```

    [32mAnswer:[0m $2018.97
    

iii. A nonconstant yield of $y(t) = 0.06 + 0.2 t e^{-t^2}$.


```python
# Question iii
q = "iii"
def yield_function(t): return 0.06 + 0.2 * t * math.exp(-t**2)

price_iii = bond.price_zero_coupon_bond_nonconstant_yield(
    face_value, years_to_maturity, yield_function)

dsp.display_answer(price_iii)
```

    [32mAnswer:[0m $2725.32
    

### Part B (3 marks)

A 10 year \$10,000 government bond has a coupon rate of 5\% payable quarterly and yields 7\%. Calculate the price.


```python
# Part b (3 marks)
face_value = 10_000
years_to_maturity = 10
coupon_rate = 0.05
interest_rate = 0.07
compounding_frequency_yr = 4

price_b = bond.price_coupon_bearing_bond_discrete(
    face_value, years_to_maturity, coupon_rate, interest_rate, compounding_frequency_yr)

dsp.display_answer(price_b)
```

    [32mAnswer:[0m $8570.29
    

## Question 2 (6 marks)

Consider the cash flow 

$$C_0 = -3x,\hspace{0.5cm} C_1 = 5,\hspace{0.5cm} C_2 = x$$

(at periods 0, 1, 2 respectively) for some $x > 0$.

## Part A (3 marks)

Apply the discount process $d(k) = (1 + r)^{-k}$ so that the present value is

$$P = \sum_{k=0}^{2} d(k) C_k$$

What is the range of $x$ such that $P > 0$ when $r = 5\%$?

\begin{split}
    0 &< P \\
    0 &< \sum_{i=0}^{2} d(k) C_k \\
    0 &< \left[(1 + 0.05)^{-0} \cdot -3x\right] + \left[(1 + 0.05)^{-1} \cdot 5\right] + \left[(1 + 0.05)^{-2} \cdot x\right] \\
    0 &< \left[1 \cdot -3x\right] + \left[\frac{5}{1 + 0.05}\right] + \left[\frac{x}{(1 + 0.05)^{2}}\right] \\
    0 &< -3x + \frac{5}{1.05} + \frac{x}{1.05^{2}} \\
    0 &< -3 \cdot 1.05^2 x + 5 \cdot 1.05 + x \\
    0 &< -2.3075 x + 5.25 \\
    2.3075 x &< 5.25 \\
    x &< \frac{5.25}{2.3075} \\
    x &\lessapprox 2.275 \\
\end{split}

Therefore, when $r = 5\%$, $P > 0$ holds when $x \lessapprox 2.275$.

We can verify this in code numerically as follows.


```python
r = 0.05
cash_flow = lambda k, x: -3*x if k == 0 else (5 if k == 1 else x)

accept_condition = lambda p: p > 0

# Function to calculate present value based on some value of x
def present_value(x: float) -> float:
    present_value = sum(cash_flow(k, x) * interest.discrete_compound_interest_discounted(r, k, 1) \
                        for k in range(2+1))
    
    return present_value

cash_flows_x: Dict[float, float] = {}
x_min = -100.0
x_max = 100.0
x_step = 0.01
accept_min_x = 0
accept_max_x = None

# Loop over a wide range of x
for x in np.arange(x_min, x_max, x_step):
    cash_flow_x = present_value(x)

    cash_flows_x[x] = cash_flow_x

    if accept_condition(cash_flow_x):
        # Min
        if not accept_min_x:
            accept_min_x = x
        elif x < accept_min_x:
            accept_min_x = x

        # Max
        if not accept_max_x:
            accept_max_x = x
        elif x > accept_max_x:
            accept_max_x = x

if accept_min_x == x_min:
    accept_min_x = 0

if accept_max_x == x_max:
    accept_max_x = math.inf

print(
    f"Range of x such that P > 0 when r = {r * 100}%: {accept_min_x} < x < {accept_max_x}")

```

    Range of x such that P > 0 when r = 5.0%: 0 < x < 2.2700000000523204
    

## Part B (3 marks)

The IRR (internal rate of return) is $r$ such that $P = 0$. For what range of $x$ will there be a unique, strictly positive IRR?

\begin{split}
    P &= \sum_{k=0}^{2} d(k) \cdot C_k \\
    0 &= \left[d(0) \cdot -3x\right] + \left[d(1) \cdot 5\right] + \left[d(2) \cdot x\right] \\
    &= -3x (1 + r)^{-0} + 5 (1 + r)^{-1} + x (1 + r)^{-2} \\
    &= -3x \cdot 1 + \frac{5}{1 + r} + \frac{x}{(1 + r)^2} \\
    &= -3x (1 + r)^2 + 5 (1 + r) + x \\
    &= -3x (1^2 + 2r + r^2) + 5 + 5r + x \\
    &= -3x - 6xr - 3xr^2 + 5 + 5r + x \\
    &= -3xr^2 + (5 - 6x)r + (x - 3x + 5) \\
    &= -3xr^2 + (5 - 6x)r + (5 - 2x)
\end{split}

As we want $r > 0$, then solve for $\Delta > 0$

\begin{split}
    0 &< \Delta \\
    0 &< (5 - 6x)^2 - 4 \cdot (-3x) \cdot (5 - 2x) \\
    0 &< (25 - 60x + 36x^2) + 12x \cdot (5 - 2x) \\
    0 &< 36x^2 - 60x + 25 + 60x - 24x^2 \\
    0 &< 12x^2 + 25
\end{split}

This will always hold $\forall x \in \mathbb{R}^+$

Therefore, if $x > 0$, then IRR $= \left\{r | P = 0\right\} > 0$.

## Question 3 (8 marks)

| Cashflows ($C_i$) | Times ($t_i$) |
| :---------------: | :-----------: |
| 2.3               | 1.0           |
| 2.9               | 2.0           |
| 3.0               | 3.0           |
| 3.2               | 4.0           |
| 4.0               | 5.0           |
| 3.8               | 6.0           |
| 4.2               | 7.0           |
| 4.8               | 8.0           |
| 5.5               | 9.0           |
| 105               | 10.0          |

<p style="text-align: center;">Table 1: Bond Cashflows</p>

In this question, consider a bond with a set of cashflows given in Table 1. Here, note that the face value $F$ is already included in the last cashflow. Let $y$ be the yield to maturity, $t_i$ be the time of the $i^{\text{th}}$ cashflow $C_i$, and $PV = 100$ be the market price of the bond at $t = 0$. Assume continuous compounding. Then $y$ solves

$$PV = \sum_{i} C_i e^{-y t_i}$$

## Part A (3 marks)

Write out the Newton iteration to compute $y_{n+1}$ from $y_n$ (see L2.49). Specifically, clearly indicate the functions $f(y)$ and $f'(y)$.

In this question

$$f(y) = \left[\sum_{t=1}^{10} C_t \cdot \beta(y, t)\right] - P = \left[\sum_{t=1}^{10}C_t \exp\left\{-y \cdot t\right\}\right] - P$$

and

$$f'(y) = \sum_{t=1}^{10} C_t \cdot \beta'(y, t) = \sum_{t=1}^{10} C_t \cdot \frac{d}{dx}\exp\left\{-y \cdot t\right\} = - \sum_{t=1}^{10}t C_t \exp\left\{-y \cdot t\right\}$$

Using these definitions, perform the following

1. Choose an intial value of $x_0$, say $x_0 = 0.05$
2. Compute the following until the termination condition

\begin{split}
    x_{n+1} &\approx x_n - \frac{f(x_n)}{f'(x_n)} \\
    &\approx x_n + \frac{\left[\sum_{t=1}^{10}C_t \exp\left\{-x_n \cdot t\right\}\right] - P}{- \sum_{t=1}^{10}t C_t \exp\left\{-x_n \cdot t\right\}}
\end{split}

3. Terminate when $|x_{n+1} - x_{n}| < \epsilon$ or $|f(x_{n+1})| < \epsilon$

## Part B (5 marks)

Implement the above Newton iteration in Matlab (I'm using Python) using the stopping criteria 

$$|y_{n+1} - y_n| < 10^{-8}.$$

Fill in Table 2 for $y_0 = 0.05$ (add rows as necessary).

In addition, try with larger values for $y_0$ and observe the accuracy and convergence speed. How does the performance change?


```python
# Part b (5 marks)
cashflows = [2.3, 2.9, 3.0, 3.2, 4.0, 3.8, 4.2, 4.8, 5.5, 105]

# Market price of the bond at t = 0
PV = 100

def f(y): return sum(
    cashflows[t-1] * interest.continuous_compound_interest_discounted(y, t) for t in range(1, len(cashflows)+1)) - PV

def f_prime(y): return - \
    sum(((t * cashflows[t]) / ((1 + y)**(t + 1)))
        for t in range(len(cashflows)))

    
eps = 1e-8

# Set initial y value
x_0 = 0.05

# Print table header
col_heads = ["$$n$$", "$$y_n$$" , "$$|y_{n}-y_{n-1}|$$"]
col_spaces = [3, 11, 17]

md_table = ""
header_row = ""
format_row = ""

for i, col_head in enumerate(col_heads):
    space = col_spaces[i]
    part = f"|{col_head:^{space}}"
    header_row += part
    middle = '-'*(max(1, len(part) - 2 - 2))
    format_row += f"| :{middle}: "

header_row += "|"
format_row += "|"

# Solve y using Newton's method given f and PV as inputs

approx, table_rows, _ = newtons.newtons_method(f, f_prime, x_0, eps, 9999999, generate_table=True, log=False, 
                                               col_spaces=col_spaces, precision=10)

md_table += header_row + "  \n"
md_table += format_row + "  \n"
md_table += "  \n".join(table_rows)

def printmd(string):
    display(Markdown(string))
    
printmd(md_table)
```


|$$n$$|  $$y_n$$  |$$|y_{n}-y_{n-1}|$$|  
| :--: | :--------: | :----------------: |  
| 0 |0.0345487861|  0.0154512139   |  
| 1 |0.0372734985|  0.0027247125   |  
| 2 |0.0369704389|  0.0003030597   |  
| 3 |0.0370078067|   3.73678e-05   |  
| 4 |0.0370032489|   4.5578e-06    |  
| 5 |0.0370038056|    5.567e-07    |  
| 6 |0.0370037376|     6.8e-08     |  
| 7 |0.0370037459|     8.3e-09     |


### Part ii: Larger values of $y_0$


```python
increment = 0.01
y_0_vals = [x for x in np.arange(0.05, 0.25+increment, increment)]

for y_0 in y_0_vals:
    print(
        f"{Fore.CYAN}y_0 = {Fore.LIGHTRED_EX}{round(y_0, 2)}{Style.RESET_ALL}", end=": ")
    approx, _, num_iterations = newtons.newtons_method(
        f, f_prime, y_0, eps, 9999999, generate_table=False, log=False)
    
    ans = f" {Fore.LIGHTGREEN_EX}{approx:.10f}{Style.RESET_ALL} in {Fore.LIGHTMAGENTA_EX}{num_iterations} iterations{Style.RESET_ALL}."

    print(ans)
```

    [36my_0 = [91m0.05[0m:  [92m0.0370037459[0m in [95m7 iterations[0m.
    [36my_0 = [91m0.06[0m:  [92m0.0370037448[0m in [95m8 iterations[0m.
    [36my_0 = [91m0.07[0m:  [92m0.0370037447[0m in [95m8 iterations[0m.
    [36my_0 = [91m0.08[0m:  [92m0.0370037447[0m in [95m8 iterations[0m.
    [36my_0 = [91m0.09[0m:  [92m0.0370037448[0m in [95m8 iterations[0m.
    [36my_0 = [91m0.1[0m:  [92m0.0370037452[0m in [95m8 iterations[0m.
    [36my_0 = [91m0.11[0m:  [92m0.0370037459[0m in [95m8 iterations[0m.
    [36my_0 = [91m0.12[0m:  [92m0.0370037448[0m in [95m9 iterations[0m.
    [36my_0 = [91m0.13[0m:  [92m0.0370037447[0m in [95m9 iterations[0m.
    [36my_0 = [91m0.14[0m:  [92m0.0370037447[0m in [95m9 iterations[0m.
    [36my_0 = [91m0.15[0m:  [92m0.0370037440[0m in [95m6 iterations[0m.
    [36my_0 = [91m0.16[0m:  [92m0.0370037457[0m in [95m9 iterations[0m.
    [36my_0 = [91m0.17[0m:  [92m0.0370037447[0m in [95m10 iterations[0m.
    [36my_0 = [91m0.18[0m:  [92m0.0370037447[0m in [95m10 iterations[0m.
    [36my_0 = [91m0.19[0m:  [92m0.0370037451[0m in [95m9 iterations[0m.
    [36my_0 = [91m0.2[0m:  [92m0.0370037448[0m in [95m11 iterations[0m.
    [36my_0 = [91m0.21[0m:  [92m0.0370037447[0m in [95m11 iterations[0m.
    [36my_0 = [91m0.22[0m:  [92m0.0370037453[0m in [95m11 iterations[0m.
    [36my_0 = [91m0.23[0m:  [92m0.0370037447[0m in [95m12 iterations[0m.
    [36my_0 = [91m0.24[0m:  [92m0.0370037458[0m in [95m12 iterations[0m.
    [36my_0 = [91m0.25[0m:  [92m0.0370037444[0m in [95m12 iterations[0m.
    

As seen above, as the initial estimate, $y_0$ is increased beyond $0.05$ (up to $0.25$), more iterations of Newton's method are required in order to achieve the same level of accuracy. In other words, for the same iteration number, a solution starting with a higher $y_0$ has a lower accuracy.

The difference in the time taken to solve is negligable here, however, so is not reported.

## Question 4

In the Constant Growth DDM model, the present value of the share is

$$PV = \sum_{t=1}^{\infty} \frac{D_t}{(1 + k)^t}$$

where $D_1, D_2, ...$ are (non-random) dividends and $k > 0$ is the required rate of return

Suppose $D_0 > 0$, $k > 0$ and $g > 0$

Derive the formula for the present value (2) when

$$D_t = D_0 (1 + g)^{\lceil \frac{t}{2} \rceil}, \hspace{0.5cm} t = 1, 2, ...$$

where $\lceil x \rceil$ is the smallest integer greater than or equal to $x$. What is the condition of $g$ so that $PV$ is finite? To get full marks, you will need to write an explicit expression (without summation).

First substitute for $D_t$ as defined in the question and expand to see the pattern

\begin{split}
    PV &= \sum_{t=1}^{\infty} \frac{D_t}{(1 + k)^t} \\
    &= \sum_{t=1}^{\infty} \frac{D_0 (1 + g)^{\lceil \frac{t}{2} \rceil}}{(1 + k)^t} \\ 
    &= \left[ D_0 \cdot \frac{(1 + g)^{\lceil \frac{1}{2} \rceil}}{(1 + k)^1} \right] + \left[ D_0 \cdot \frac{(1 + g)^{\lceil \frac{2}{2} \rceil}}{(1 + k)^2} \right] + \left[ D_0 \cdot \frac{(1 + g)^{\lceil \frac{3}{2} \rceil}}{(1 + k)^3} \right] + \left[ D_0 \cdot \frac{(1 + g)^{\lceil \frac{4}{2} \rceil}}{(1 + k)^4} \right] + \cdots \\
    &= \left[ D_0 \cdot \frac{(1 + g)^{1}}{(1 + k)^1} \right] + \left[ D_0 \cdot \frac{(1 + g)^{1}}{(1 + k)^2} \right] + \left[ D_0 \cdot \frac{(1 + g)^{2}}{(1 + k)^3} \right] + \left[ D_0 \cdot \frac{(1 + g)^{2}}{(1 + k)^4} \right] + \cdots
\end{split}

Now consider, splitting up the geometric series into sub series where

* the exponent on the numerator is half the exponent on the denominator; and
* the above is not the case


We then have

\begin{split}
    PV &= \left\{ \left[ D_0 \cdot \frac{(1 + g)^{1}}{(1 + k)^2} \right] + \left[ D_0 \cdot \frac{(1 + g)^{2}}{(1 + k)^4} \right] + \cdots \right\} + \left\{ \left[ D_0 \cdot \frac{(1 + g)^{1}}{(1 + k)^1} \right] + \left[ D_0 \cdot \frac{(1 + g)^{2}}{(1 + k)^3} \right] + \cdots \right\} \\
    &=  D_0 \left\{ \left[ \frac{(1 + g)^{1}}{(1 + k)^2} \right] + \left[ \frac{(1 + g)^{2}}{(1 + k)^4} \right] + \cdots \right\} + D_0 \left\{ \left[ \frac{(1 + g)^{1}}{(1 + k)^1} \right] + \left[ \frac{(1 + g)^{2}}{(1 + k)^3} \right] + \cdots \right\} \\
    &=  D_0 \left\{ \left[ \frac{(1 + g)^{1}}{(1 + k)^2} \right] + \left[ \frac{(1 + g)^{2}}{(1 + k)^4} \right] + \cdots \right\} + D_0 (1 + k) \left\{ \left[ \frac{(1 + g)^{1}}{(1 + k)^2} \right] + \left[ \frac{(1 + g)^{2}}{(1 + k)^4} \right] + \cdots \right\} \\
    &= \sum_{t=1}^{\infty} D_0 \left[ \frac{1 + g}{(1 + k)^2} \right]^{t} + \sum_{t=1}^{\infty} D_0 (1 + k) \left[ \frac{1 + g}{(1 + k)^2} \right]^{t} \\
    &= \sum_{t=1}^{\infty} D_0 \frac{1 + g}{(1 + k)^2} \left[ \frac{1 + g}{(1 + k)^2} \right]^{t-1} + \sum_{t=1}^{\infty} D_0 (1 + k) \frac{1 + g}{(1 + k)^2} \left[ \frac{1 + g}{(1 + k)^2} \right]^{t-1} \\
    &= \sum_{t=1}^{\infty} D_0 \frac{1 + g}{(1 + k)^2} \left[ \frac{1 + g}{(1 + k)^2} \right]^{t-1} + \sum_{t=1}^{\infty} D_0 \frac{1 + g}{1 + k} \left[ \frac{1 + g}{(1 + k)^2} \right]^{t-1} \\
\end{split}

These are both valid geometric series. Now apply the infinite geometric series formula

$$\sum_{n=1}^{\infty} a r^{n - 1} = S_n =\frac{a}{1-r}$$

\begin{split}
    PV &= \frac{D_0 \frac{1 + g}{(1 + k)^2}}{1 - \frac{1 + g}{(1 + k)^2}} + \frac{D_0 \frac{1 + g}{1 + k}}{1 - \frac{1 + g}{(1 + k)^2}} \\
    &= \frac{D_0 \frac{1 + g}{(1 + k)^2} + D_0 \frac{1 + g}{1 + k}}{1 - \frac{1 + g}{(1 + k)^2}} \\
    &= \frac{D_0 \frac{1 + g}{1 + k} \left[\frac{1}{1 + k} + 1\right]}{1 - \frac{1 + g}{(1 + k)^2}} \\
\end{split}

Condition of $g$ for when $PV$ is finite.

From the geometric series, $PV$ will be finite when $|r| < 1$, where $r = \frac{1 + g}{(1 + k)^2}$. So solve

\begin{split}
    |r| &< 1 \\
    \left|\frac{1 + g}{(1 + k)^2} \right| &< 1 \\
    -(1 + k)^2 < 1 + g &< (1 + k)^2 \\
    -(1 + 2k + k^2) - 1 < g &< (1 + 2k + k^2) - 1 \\
    -(2 + 2k + k^2) < g &< k^2 + 2k \\
    -2 - 2k - k^2 < g &< k(k + 2) \\
\end{split}

Since $g > 0$ and $k > 0$, we do not need to consider the lower bound. Thus for $PV$ to be finite ($PV < \infty$), the following condition must hold

$$g < k(k + 2)$$
