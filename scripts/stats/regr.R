library(tidyverse)
library(broom)
root = "../../data/predictions/cleaned/1pct_x_z3_y/"
r = read.csv(paste0(root, "right/right_joint_space_raw.csv"))
l = read.csv(paste0(root, "left/left_joint_space_raw.csv"))
rh = read.csv("right_standing_height.csv")
lh = read.csv("left_standing_height.csv")
lh = subset(lh, select=c(eid, file, height))
rxy = read.csv(paste0(root,"right/right_joint_space.csv"))
lxy = read.csv(paste0(root,"left/left_joint_space.csv"))
rxy = subset(rxy, select=c(file, x, y, xmax))
lxy = subset(lxy, select=c(file, x, y, xmax))
r = merge(r, rxy, by = "file")
l = merge(l, lxy, by = "file")

right = merge(r, rh, by = "file")
left = merge(l, lh, by = "file")
write.csv(right, "../../data/predictions/cleaned/1pct_x_z3_y/right/right_joint_space_raw.csv", row.names = FALSE)
write.csv(left, "../../data/predictions/cleaned/1pct_x_z3_y/left/left_joint_space_raw.csv", row.names = FALSE)

ru <- unique(right$x)
lu <- unique(left$x)

autoregr <- function(data, uniques, namestr) {
  
  for (xval in uniques) {
    df <- subset(data, x == xval)
    modl <- lm(xmax~height, data=df)
    xv <- as.character(xval)
    fname <- paste0(namestr, "_", xv, "_xmax_height.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

autoregr(right, ru, "r")
autoregr(left, lu, "l")
