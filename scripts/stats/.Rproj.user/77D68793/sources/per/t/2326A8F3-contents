
library(tidyverse)
library(broom)
# Joint Space
root = "../../data/predictions/cleaned/1pct_x_z3_y_iqr/"
right = read.csv(paste0(root, "right/right_joint_space_raw.csv"))
left = read.csv(paste0(root, "left/left_joint_space_raw.csv"))
rfta = read.csv(paste0(root, "right/right_joint_space_norm_by_ft_average.csv"))
rfta <- rfta[, c("file", "fem_tib_average")]
lfta = read.csv(paste0(root, "left/left_joint_space_norm_by_ft_average.csv"))
lfta <- lfta[, c("file", "fem_tib_average")]
# Joint Area
root = 'replicates/data/'
right = read.csv(paste0(root, 'right/right_joint_area.csv'))
left = read.csv(paste0(root, 'left/left_joint_area.csv'))

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

# right <- merge(right, rfta, by = "file")
# left <- merge(left, lfta, by = "file")

r_groups <- read.csv('./replicates/data/right_xy_groups.csv')
colnames(r_groups)[1] <- "file"
r_groups <- r_groups[, c("file", "xy_group")]
l_groups <- read.csv('./replicates/data/left_xy_groups.csv')
colnames(l_groups)[1] <- "file"
l_groups <- l_groups[, c("file", "xy_group")]

right_groups <- merge(right, r_groups, by = "file")
left_groups <- merge(left, l_groups, by = "file")



right_groups <- read.csv('../../data/predictions/cleaned/right_joint_space_xygroup.csv')
left_groups <- read.csv('../../data/predictions/cleaned/left_joint_space_xygroup.csv')

ru <- unique(right_groups$xy_group)
lu <- unique(left_groups$xy_group)

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

# area, x values
autoregr_zero <- function(data, uniques, namestr) {
  
  for (xval in uniques) {
    df <- subset(data, x == xval)
    modl <- lm(all_area_average ~ 0 + combined_area_i2, data=df)
    xv <- as.character(xval)
    fname <- paste0(namestr, "_", xv, "_zero_area.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

colnames(right)
ca <- read.csv('../../data/combined_leg_area.csv')
right <- merge(ca, right, by = "eid")
left <- merge(ca, left, by = "eid")

ru <- unique(right$x)
lu <- unique(left$x)

autoregr_zero(right, ru, "r")
autoregr_zero(left, lu, "l")


# area, AB group
autoregr_zero <- function(data, uniques, namestr) {
  
  for (xval in uniques) {
    df <- subset(data, AB_groups == xval)
    modl <- lm(all_area_average ~ 0 + combined_area_i2, data=df)
    xv <- as.character(xval)
    fname <- paste0(namestr, "_", xv, "_zero_area.csv")
    print(fname)
    tidy_modl <- tidy(modl)
    print(summary(modl))
    
    write.csv(tidy_modl, fname)
    
  }
}

colnames(right)
ca <- read.csv('../../data/combined_leg_area.csv')
right <- merge(ca, right, by = "eid")
left <- merge(ca, left, by = "eid")

rAB <- read.csv(paste0(root, 'right/right_AB.csv'))
lAB <- read.csv(paste0(root, 'left/left_AB.csv'))


rAB <- rAB[, c('file', 'AB_groups')]
lAB <- lAB[, c('file', 'AB_groups')]

right <- merge(rAB, right, on = "file")
left <- merge(lAB, left, on = "file")
ru <- unique(right$AB_groups)
lu <- unique(left$AB_groups)

autoregr_zero(right, ru, "r")
autoregr_zero(left, lu, "l")
colnames(right)

rxy <- read.csv('right_joint_space_xygroup_raw.csv')
lxy <- read.csv('left_joint_space_xygroup_raw.csv')

rxy <- rxy[, c('file', 'xy_group')]
lxy <- lxy[, c('file', 'xy_group')]
right <- merge(rxy, right, on = "file")
left <- merge(lxy, left, on = "file")

write.csv(right, "replicates/data/right_joint_area_AB_groups.csv", row.names = FALSE)
write.csv(left, "replicates/data/left_joint_area_AB_groups.csv", row.names = FALSE)
