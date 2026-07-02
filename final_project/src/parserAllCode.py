'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
'''

import rpy2.robjects as robjects

yeimport rpy2.robjects.packages as rpackages

# import R's "utils" package
utils = rpackages.importr('utils')

#install hoopR
utils.chooseCRANmirror(ind=1)
utils.install_packages("hoopR")
hoopR = rpackages.importr('hoopR')

import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as ro


'''
chromedriver_autoinstaller.install()

options = Options()
options.headless = True

driver = webdriver.Chrome(options = options)
driver.close()
'''



win_prob = pd.DataFrame()
with localconverter(ro.default_converter + pandas2ri.converter):
    win_prob = ro.conversion.rpy2py(hoopR.espn_nba_wp(game_id = 401468299))




newdf <- transform(newdf, winpb_home= get_winp_home(game_id))
rlang::last_error()
head(newdf)
print(get_winp_home(401360736))
typeof(newdf[1,'game_id'])
newdf$winpb_home <- with(newdf,get_winp_home(as.integer(game_id)))

typeof(newdf[1,'game_id'])
winProbList_home = c()
for (row in 1:nrow(newdf)) 
{
  winProbList <- append(winProbList,get_winp_home(newdf[row,"game_id"]))
}  
newdf$winpb_home <- winProbList 
length(winProbList)




