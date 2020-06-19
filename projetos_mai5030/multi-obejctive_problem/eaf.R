setwd('/Users/brunofbessa/Documents/study/mestrado/MAI5030/projetos_mai5030/multi-obejctive_problem')
df = read.csv2('nsgaii.csv', sep=',', header=TRUE)
df$f1 = as.numeric(df$f1)
df$f2 = as.numeric(df$f2)
df$run = as.numeric(df$run)


library(eaf)
eafplot(df)
