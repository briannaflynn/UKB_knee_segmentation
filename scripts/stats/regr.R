
library(tidyverse)
library(broom)

root = "../../data/predictions/cleaned/1pct_x_z3_y_iqr/"
right = read.csv(paste0(root, "right/right_joint_space_raw.csv"))
left = read.csv(paste0(root, "left/left_joint_space_raw.csv"))
rfta = read.csv(paste0(root, "right/right_joint_space_norm_by_ft_average.csv"))
rfta <- rfta[, c("file", "fem_tib_average")]
lfta = read.csv(paste0(root, "left/left_joint_space_norm_by_ft_average.csv"))
lfta <- lfta[, c("file", "fem_tib_average")]
# rh = read.csv("right_standing_height.csv")
# lh = read.csv("left_standing_height.csv")
# rh = subset(rh, select=c(file, height))
# lh = subset(lh, select=c(file, height))
# # rxy = read.csv(paste0(root,"right/right_joint_space.csv"))
# # lxy = read.csv(paste0(root,"left/left_joint_space.csv"))
# # rxy = subset(rxy, select=c(file, x, y, xmax))
# # lxy = subset(lxy, select=c(file, x, y, xmax))
# # r = merge(r, rxy, by = "file")
# # l = merge(l, lxy, by = "file")
# right = merge(right, rh, by = "file")
# left = merge(left, lh, by = "file")
# write.csv(right, paste0(root, "right/right_joint_space_raw.csv"), row.names = FALSE)
# write.csv(left, paste0(root, "left/left_joint_space_raw.csv"), row.names = FALSE)

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

autoregr_zero <- function(data, uniques, namestr) {
  
  for (xval in uniques) {
    df <- subset(data, x == xval)
    modl <- lm(xmax ~ 0 + height, data=df)
    xv <- as.character(xval)
    fname <- paste0(namestr, "_", xv, "_zero_xmax_height.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

autoregr_zero(right, ru, "r")
autoregr_zero(left, lu, "l")


autoregr_zero <- function(data, uniques, namestr) {
  
  for (xval in uniques) {
    df <- subset(data, x == xval)
    modl <- lm(xmax ~ 0 + height, data=df)
    xv <- as.character(xval)
    fname <- paste0(namestr, "_", xv, "_zero_xmax_height.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

right$right <- TRUE
left$right <- FALSE
right <- merge(right, rfta, by = "file")
left <- merge(left, lfta, by = "file")
both <- rbind(right, left)
groups <- read.csv('./replicates/data/both_xy_groups.csv')
colnames(groups)[1] <- "file"

data <- merge(both, groups, by = "file")
data
g <- unique(data$Group)

autoregr_zero <- function(data, uniques, namestr) {
  
  for (val in uniques) {
    df <- subset(data, Group == val)
    modl <- lm(fem_tib_average ~ 0 + height, data=df)
    xv <- as.character(val)
    fname <- paste0(namestr, "_", xv, "_zero_height.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

autoregr_zero(data, g, "xy_groups")

# write.csv(data, "both_joint_space_raw.csv", row.names = FALSE)

right <- merge(right, rfta, by = "file")
left <- merge(left, lfta, by = "file")

r_groups <- read.csv('./replicates/data/right_xy_groups.csv')
colnames(r_groups)[1] <- "file"
r_groups <- r_groups[, c("file", "xy_group")]
l_groups <- read.csv('./replicates/data/left_xy_groups.csv')
colnames(l_groups)[1] <- "file"
l_groups <- l_groups[, c("file", "xy_group")]

right_groups <- merge(right, r_groups, by = "file")
left_groups <- merge(left, l_groups, by = "file")

ru <- unique(right_groups$xy_group)
lu <- unique(left_groups$xy_group)

right_groups
left_groups

autoregr_zero <- function(data, uniques, namestr) {
  
  for (val in uniques) {
    df <- subset(data, xy_group == val)
    modl <- lm(fem_tib_average ~ 0 + height, data=df)
    xv <- as.character(val)
    fname <- paste0(namestr, "_", xv, "_zero_height.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

autoregr_zero(right_groups, ru, "right_xy_regr")
autoregr_zero(left_groups, lu, "left_xy_regr")

write.csv(right_groups, "right_joint_space_xygroup_raw.csv", row.names = FALSE)
write.csv(left_groups, "left_joint_space_xygroup_raw.csv", row.names = FALSE)
