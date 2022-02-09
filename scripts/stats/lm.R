library(tidyverse)
library(broom)

root = "../../data/predictions/cleaned/1pct_x_z3_y_iqr/"
right = read.csv(paste0(root, "right/right_joint_space_raw.csv"))
left = read.csv(paste0(root, "left/left_joint_space_raw.csv"))
rfta = read.csv(paste0(root, "right/right_joint_space_norm_by_ft_average.csv"))
# rfta <- rfta[, c("file", "fem_tib_average")]
lfta = read.csv(paste0(root, "left/left_joint_space_norm_by_ft_average.csv"))
# lfta <- lfta[, c("file", "fem_tib_average")]
rfta

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_space_norm_by_ft_average.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_space_norm_by_ft_average.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"

inst_data <- merge(inst_rfta, inst_lfta, by = "eid")


inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
m1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_2, data = inst_rfta)
summary(m1)

m1.0 <- lm(left_quad_all_av_norm_3 ~ left_quad_all_av_norm_2 * left_x_2, data = inst_lfta)
summary(m1.0)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_space_zero_norm_by_height.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_space_zero_norm_by_height.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"

inst_data <- merge(inst_rfta, inst_lfta, by = "eid")


inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
print("joint_space_zero_norm_by_height.csv")
m1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
print("joint_space_zero_norm_by_height.csv")
m1.0 <- lm(left_quad_all_av_norm_3 ~ left_quad_all_av_norm_2 * left_x_2, data = inst_lfta)
summary(m1.0)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_space_xygroup_zero_ratio_norm_by_height.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_space_xygroup_zero_ratio_norm_by_height.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"

inst_data <- merge(inst_rfta, inst_lfta, by = "eid")


inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
print("joint_space_xygroup_zero_ratio_norm_by_height.csv")
m1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
print("joint_space_xygroup_zero_ratio_norm_by_height.csv")
m1.0 <- lm(left_quad_all_av_norm_3 ~ left_quad_all_av_norm_2 * left_x_2, data = inst_lfta)
summary(m1.0)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_space_xygroup_zero_norm_by_height.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_space_xygroup_zero_norm_by_height.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"

inst_data <- merge(inst_rfta, inst_lfta, by = "eid")


inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_data$right_x_2 <- factor(inst_data$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
print("joint_space_xygroup_zero_norm_by_height.csv")
m1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
print("joint_space_xygroup_zero_norm_by_height.csv")
m1.0 <- lm(left_quad_all_av_norm_3 ~ left_quad_all_av_norm_2 * left_x_2, data = inst_lfta)
summary(m1.0)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta %>%
  mutate(joint_px_size = paste0(right_x_2, "_", right_x_3)) %>%
  group_by(joint_px_size) %>%
  summarise(total = n())

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_space_xygroup_zero_ratio_norm_by_height.csv')
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_space_xygroup_zero_ratio_norm_by_height.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"
inst_rfta
inst_data <- merge(inst_rfta, inst_lfta, by = "eid")
inst_data

inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
m1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_2, data = inst_rfta)
summary(m1)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_area.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_area.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"
inst_rfta
inst_data <- merge(inst_rfta, inst_lfta, by = "eid")
inst_data

inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
m1 <- lm(right_quad_all_area_norm_3 ~ right_quad_all_area_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
m10 <- lm(left_quad_all_area_norm_3 ~ left_quad_all_area_norm_2 * left_x_2, data = inst_lfta)
summary(m10)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_zero_norm_by_DXA_area.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_zero_norm_by_DXA_area.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"
inst_rfta
inst_data <- merge(inst_rfta, inst_lfta, by = "eid")
inst_data

inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
print("inst_joint_zero_norm_by_DXA_area.csv")
m1 <- lm(right_quad_all_area_norm_3 ~ right_quad_all_area_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
print("inst_joint_zero_norm_by_DXA_area.csv")
m10 <- lm(left_quad_all_area_norm_3 ~ left_quad_all_area_norm_2 * left_x_2, data = inst_lfta)
summary(m10)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_area_AB_groups_zero_norm_by_DXA_area.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_area_AB_groups_zero_norm_by_DXA_area.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"
inst_rfta
inst_data <- merge(inst_rfta, inst_lfta, by = "eid")
inst_data

inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
print("inst_joint_area_AB_groups_zero_norm_by_DXA_area.csv")
m1 <- lm(right_quad_all_area_norm_3 ~ right_quad_all_area_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
print("inst_joint_area_AB_groups_zero_norm_by_DXA_area.csv")
m10 <- lm(left_quad_all_area_norm_3 ~ left_quad_all_area_norm_2 * left_x_2, data = inst_lfta)
summary(m10)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)

inst_rfta = read.csv('./replicates/data/right/inst_right_joint_area_AB_groups_zero_ratio_norm_by_DXA_area.csv') 
inst_lfta = read.csv('./replicates/data/left/inst_left_joint_area_AB_groups_zero_ratio_norm_by_DXA_area.csv')

colnames(inst_rfta) <- paste("right", colnames(inst_rfta), sep = "_")
colnames(inst_lfta) <- paste("left", colnames(inst_lfta), sep = "_")
colnames(inst_rfta)[which(names(inst_rfta) == "right_eid")] <- "eid"
colnames(inst_lfta)[which(names(inst_lfta) == "left_eid")] <- "eid"
inst_rfta
inst_data <- merge(inst_rfta, inst_lfta, by = "eid")
inst_data

inst_rfta$right_x_2 <- factor(inst_rfta$right_x_2)
inst_lfta$left_x_2 <- factor(inst_lfta$left_x_2)
print("ratio_norm_by_DXA_area")
m1 <- lm(right_quad_all_area_norm_3 ~ right_quad_all_area_norm_2 * right_x_2, data = inst_rfta)
summary(m1)
print("ratio_norm_by_DXA_area")
m10 <- lm(left_quad_all_area_norm_3 ~ left_quad_all_area_norm_2 * left_x_2, data = inst_lfta)
summary(m10)

m2 <- lm(right_quad_all_av_norm_2 ~ left_quad_all_av_norm_2 * right_x_2, data = inst_data)
summary(m2)

m1.1 <- lm(right_quad_all_av_norm_3 ~ right_quad_all_av_norm_2 * right_x_3, data = inst_rfta)
summary(m1.1)

m2.1 <- lm(right_quad_all_av_norm_2 ~ 0 + left_quad_all_av_norm_2, data = inst_data)
summary(m2.1)



