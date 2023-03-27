library(tidyverse)
library(patchwork)
library(viridis)

###################################
###       Data                  ###
###################################
data <- read_tsv("pattern_distribution.tsv")

################################################
#####       Distribution Plots             #####
################################################
dist <- data %>% 
  ggplot(aes(reorder(ID,-Count), Count , col=Trimming, shape=Trimming)) +
  geom_point(size = 1.2, alpha=0.6) +
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  scale_color_viridis(discrete = TRUE, end = 0.8) +
  facet_wrap(~Language, scales="free", ncol=2) + 
  ylab("Sites in pattern") + xlab("Pattern") +
  labs(color="Trimming strategy", shape = "Trimming strategy") +
  theme(legend.position = 'bottom') +
  guides(colour = guide_legend(
    override.aes = list(size = 5, alpha=1))) +
  expand_limits(x = -4)

ggsave("alignment_distribution.png", dist, scale = 0.62, width = 2000, height = 4000, units = "px")

# does not work well, but small differences are noticable
violin_init <- data %>% 
  ggplot(aes(y = log(Count), x = Trimming)) +
  geom_violin(aes(fill = Trimming)) +
  geom_boxplot(width = 0.5, 
               outlier.size = 1, outlier.color = "black", outlier.alpha = 0.3) +
  facet_wrap(~Language, ncol = 4, scales="free") +
  scale_fill_viridis(discrete = TRUE, end = 0.7) +
  scale_x_discrete(label = NULL, name = NULL) +
  theme_grey(base_size = 11) +
  theme(legend.position = 'bottom', legend.title = "Trimming strategy")+
  guides(colour = guide_legend(override.aes = list(size = 10)))

