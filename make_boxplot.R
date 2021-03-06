#!/usr/bin/env Rscript

# Jen's script for auto-generation of boxplot
# January 31st, 2017 (Tuesday)

# to be used with .csv files generated by the timeline analysis code
# version 5 or higher (for whole files only, not residue .csv files)

# assign arguments to args
args = commandArgs(trailingOnly = TRUE)

# assign error if no arguments are given
if (length(args) <= 2) {
    stop("Need 3 arguments: (1) input csv file, (2) simulation name, and (3) length of simulation (ns).n", call.=FALSE)
}

# Assign variables for titles
jtitle <- args[2]
jxaxis <- "Secondary Structure"
jyaxis <- "% of Simulation Spent as Secondary Structure"
jsubtitle <- paste("Based on 5ns intervals from a ", args[3], "ns Simulation", sep='')
oname <- paste(substr(args[1], 1, nchar(args[1])-4), "_boxplot.pdf", sep='')


# file directory (where csv is located)
fdir <- getwd()
# script directory (in case needed)
sdir <- "/home/jgarne01/Documents/jen_scripts"
# assign filename
fname <- paste(fdir, '/', args[1], sep='')
# read in csv file
bplot <- read.csv(fname, header=TRUE)
# remove first column (specifies time frames, unimportant)
bplot <- bplot[, 2:8]
# assign list of colours (THEBIGC)
# Turn, Alpha Helix, Ext. Config., Isol. Bridge, Pi-Helix, 3-10 Helix, Coil
bcols <- c("cyan", "pink", "yellow", "gold", "red", "blue", "white")
# save to outpute name
pdf(oname)
# make boxplot
boxplot(bplot, col=bcols, main=jtitle, xlab=jxaxis, ylab=jyaxis)
# add subtitle
mtext(jsubtitle)
# close making things (?) lol
dev.off()
