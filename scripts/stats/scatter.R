library(tidyverse)
library(ggplot2)
library(ggpmisc)
data <- read.csv("./replicates/data/left/inst_left_joint_space_norm_by_ft_average.csv")

x <- data$quad_all_av_norm_2
y <- data$quad_all_av_norm_3
df <- data.frame(x, y)
lm(y ~ 0 + x)
cor(x, y)
p <- ggplot(data = df, aes(x = x, y = y)) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = y ~ 0 + x) +
  geom_point()

lm_eqn <- function(df){
  m <- lm(y ~ 0 + x, df);
  eq <- c(a = format(unname(coef(m)[1]), digits = 2),
                        b = format(unname(coef(m)[2]), digits = 2),
                        r2 = format(summary(m)$r.squared, digits = 3))
  paste0("y = ", eq[1], "x + 0, R^2 = ", eq[3])
}

p1 <- p + geom_text(aes(x = 0.06, y = 0.1, label = lm_eqn(df)), stat = "unique")
p1

data <- read.csv("./replicates/data/left/inst_left_joint_space_norm_by_ft_average.csv")

x <- data$quad_all_av_norm_2
y <- data$quad_all_av_norm_3
df <- data.frame(x, y)

lm(y ~ x)

p <- ggplot(data = df, aes(x = x, y = y)) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = y ~ x) +
  geom_point()

lm_eqn <- function(df){
  m <- lm(y ~ x, df);
  eq <- c(a = format(unname(coef(m)[1]), digits = 2),
          b = format(unname(coef(m)[2]), digits = 2),
          r2 = format(summary(m)$r.squared, digits = 3))
  paste0("y = ", eq[1], "x + ", eq[2], ", R^2 = ", eq[3])
}

p1 <- p + geom_text(aes(x = 0.06, y = 0.1, label = lm_eqn(df)), stat = "unique")
p1

x <- data$quad_all_av_2
y <- data$quad_all_av_3
df <- data.frame(x, y)
lm(y~0+x)
lm(y~x)
cor(x, y)

p <- ggplot(data = df, aes(x = x, y = y)) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = y ~ 0 + x) +
  geom_point()

lm_eqn <- function(df){
  m <- lm(y ~ 0 + x, df);
  eq <- c(a = format(unname(coef(m)[1]), digits = 2),
          b = format(unname(coef(m)[2]), digits = 2),
          r2 = format(summary(m)$r.squared, digits = 3))
  paste0("y = ", eq[1], "x + 0, R^2 = ", eq[3])
}

p1 <- p + geom_text(aes(x = 20, y = 30, label = lm_eqn(df)), stat = "unique")
p1


