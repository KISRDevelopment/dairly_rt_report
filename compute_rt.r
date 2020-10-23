library(R0)

args <- commandArgs(trailingOnly = TRUE)

input_path <- args[1]
gt_distrib <- args[2]
gt_distrib_mean <- as.numeric(args[3])
gt_distrib_std <- as.numeric(args[4])
output_path <- args[5]

gt_params = c(gt_distrib_mean, gt_distrib_std)

# ML Estimate
covid <- read.table(input_path, sep=",", header=TRUE)
n_days <- nrow(covid)
COVID19<-covid$cases
epid.count=COVID19
GT.mers<-generation.time(gt_distrib, gt_params)
est.GT(serial.interval=COVID19,request.plot=FALSE)

ml_res.R<-est.R0.ML(COVID19, GT=GT.mers, begin=as.integer(1), end=n_days, range=c(0.01,100))
mean_R0 <- ml_res.R$R
mean_R0_ci <- ml_res.R$conf.int

# R(t)
res.R<-est.R0.TD(COVID19, GT=GT.mers, begin=as.integer(1), end=n_days, nsim=10000)
pred_results<-cbind(res.R$epid$incid, res.R$pred, res.R$R, res.R$conf.int, mean_R0, mean_R0_ci[1], mean_R0_ci[2])
write.csv(pred_results, output_path)

