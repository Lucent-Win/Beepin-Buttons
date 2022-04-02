import tkinter as tk
from threading import Timer

'''
Container module for every UI element of the application. 
'''



class lockbar(tk.Toplevel):
	'''
	Creates an always-on-top window that displays status of lock keys. 
	(Caps lock, num lock, scroll lock)
	'''

	def __init__(self, window):		
		super().__init__(window)

		self.interval = 0.48 #time between flashes	
		# if the key is on system wide		
		self.caps_on = True
		self.num_on = True
		self.scroll_on = True
		# should the key not flash?
		self.ignore_caps = False
		self.ignore_num = False
		self.ignore_scroll = False

		self.show_on_img = True # boolean for switching images
		self.img_caps_on = tk.PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAAAgCAYAAACFM/9sAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/E0XxQQoFRRS2iGIRQRTEUiKYJlokEYzabDYvIYnL7gYJtoKNRcBCtPFV+A+0FWwVBEERRKz8Ab4aCesdE0gQnWX2fpyZc5k5A55wzsjbzWOQLzhWJBTUFuNLWusLXgbxEaBXN2xzLjob49/xeUeTqrejqtf/+/4cHcmUbUBTm/CkYVqO8LRweN0xFW8L9xhZPSl8KByw5IDCV0pPVPlZcabK74qtWGQGPKqnlmngRAMbWSsvPCLsz+eKRu086iadqcJCVGq/zAFsIoQIopGgyCo5HEalFiSzv31jP7551sRjyN+khCWODFnxBkQtSteU1LToKflylFTuv/O00xPj1e6dQWh5ct23IWjdgUrZdb+OXLdyDN5HuCjU/WuS09SH6OW65j8A3yacXda1xC6cb0Hfg6lb+o/klelJp+H1FLri0H0D7cvVrGrrnNxDbEOe6Br29mFY9vtWvgEgR2gZpwP8dwAAAAlwSFlzAAAPYQAAD2EBqD+naQAABUdJREFUaAXtWd1rXEUUP3d3s9lkkzSp1mpMMKQ+pCKSCJEa8QNBhBYfFMS++uBLKr5IS2mLVsGC4AeK5k+wSB4U/AAJffChrRhrow9tRJNWE4vbaHeT3ez3h/c3N+fe2bv37p3da6Sue2D3zp2Zc+bMb86cOWeuRjr98Hjo4H3R4mmU26SGQIXoncBn9LJWeYqO6CxvqrG1e9kQeBcA6mC2qVkEQsy47+IAF9tPBQS+mYiLXiaAeIsVApQqaQrs/+8uPUFr01YB2Ah4HZUijXfn6cAtBRPNs+shupwO0bViiMpa0KxvtYKMUxWAKhMNVEr0ynCKDg1bwDGfXLfr/K1c3dLPhgCE1Z27f51GIoYJn00E6fQfHbScDQiQJvuK9PxgwWxvaeS2JtcQgLP3JE1w9i9003ymuwqj+QzRTIxoKJirqm/lF2UAJ7vS9FB/SWDx8IUoLea7XHFZLXW6trVagzKAM2O6eemEbVsPPC+Apndv0GujedduH6500MnVHa7tJ4fWhf/lHeAk72pWo6d/7KF6CwmDwJzYHdkHZPn2evu7EoA7tbw50NGliF1GQ+8MHhZiIWn4TggY7y0LC8dBdFs4QdPL/XXl9ocqNDOaoGd3F0U/AA8CP0C5+ECSBs8FqaDVTvGJ3k366F7LINiPj0bKtDdaEroIYQp/tdIdmPZEDCXRtJTTFfURKmJlL6Q7HcOc5wZS9MFYVoBy6tdcXQs6dXdWAAXgXl/pMeW9sVKka1MJMYsXbtetLNZXMyMG78XFCH0c7zHb4cPJiI/NOq+CZQJ1emJlmJxWlNtUnjh43GJEeTJ3hA1/6yYTVgYAsN1ledAP9SC2djcZn8f9+2olAGHWNxvBBciAy/rNJcLma5Rq41VuPDyU5mLTTyUAm5buwYjJ2X8eLGaz7D/Nyq1CrmL5mIGgtXu436vLBsDwl/MTfxF8ImLcZkjJB14vWAo1M4jMA0WPD286ZjJyPz9lHQ6THa5g1TgvzDr4xZ/TxkECV2D4xAzh9D72S4TObESq3ILJ6FBQAnB+A92M0AMWIyvoINO1yp7JwBIM2RbLl+P+t5VsTUmXy5G5ZFQ/pTvpsb4cHRrKiwhABnPi2966hxhrrATgUtbqNtWbp7mktcIsSOX53p6UODmx0lPf73AMMYj8AxjWrNuSlbylu11HHDhzSf13OSq28DM7syIKQL96YZAsR8kH3qiEhXmDEeFDs8QxG7aJ39O8ng5YZCbV3QJ9cCiNnLeCeNw2eZESgBAyvWikbjBzZAN+KFF09qn/VA7Ni8zhTCO6qgLOMpUBRPw2GzO2A06vT/fGxaUBrreY4B/HwhmRIXCd/MTWBR0fyZHMhzJSMmwbVULmIvs68GF8ZCdYZIw1e8M5X0dm5UYI5pkuZbxdlbuDYCnS00ivjPQJFwv1Jjy9LDFuFWHFOCTAG5uKE7IITuHQhReIt3qtBKsGMpBxAKgv1kJ0YFdRAIce7GPlANviJPpp34b5ijGv57UqPdAI61WxxoYAhGCAiDTr2F0ZMw9FPRMU+mTNeeVgxfsX9CuvrSQelgzChAEu2pHkqwDI48HaZDlvXe0UlucGHo8HPpB9LOh/4ko3we+rkPlVDh+VlrI3/zU838bwrQ22MU5dFWtRAUS1z9qDf4quDVug6gD/Vj+cnu7J2vZroXyIbL8q/80R2gD6XLc2gD4BrPKB+GAsf/P0KXtb2PHtGcTPbRnEQyh/WNcTgor2+5OBrwfD5Uc8eNrNNgR+ywXp7dWuycCdX5Uf3SxpB23t7VcPBM7EO156/1Lqu78BBuIDXs65MdsAAAAASUVORK5CYII=')
		self.img_num_on = tk.PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAAAgCAYAAACFM/9sAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/E0XxQQoFRRS2iGIRQRTEUiKYJlokEYzabDYvIYnL7gYJtoKNRcBCtPFV+A+0FWwVBEERRKz8Ab4aCesdE0gQnWX2fpyZc5k5A55wzsjbzWOQLzhWJBTUFuNLWusLXgbxEaBXN2xzLjob49/xeUeTqrejqtf/+/4cHcmUbUBTm/CkYVqO8LRweN0xFW8L9xhZPSl8KByw5IDCV0pPVPlZcabK74qtWGQGPKqnlmngRAMbWSsvPCLsz+eKRu086iadqcJCVGq/zAFsIoQIopGgyCo5HEalFiSzv31jP7551sRjyN+khCWODFnxBkQtSteU1LToKflylFTuv/O00xPj1e6dQWh5ct23IWjdgUrZdb+OXLdyDN5HuCjU/WuS09SH6OW65j8A3yacXda1xC6cb0Hfg6lb+o/klelJp+H1FLri0H0D7cvVrGrrnNxDbEOe6Br29mFY9vtWvgEgR2gZpwP8dwAAAAlwSFlzAAAPYQAAD2EBqD+naQAAAyZJREFUaAVjZACCi04sEXrcf5aD2KOAuBD4z8DQx7SZoZjxvy9DGVBLJ3HaRlWhhUA/KACBgTkKyA0BFphGi/OCMOYoTUQInDB8D1YFD0AQ7+VvJoYvfxmJ0D6ylfAwIzItSgDiCzxTzm/wUDv9nQvORmfA1OFTg65nqPGRwwklAPF5ZJsBIgANTzEzPPnLjlU5TJ3ocdyBjFXjEBVkIsfdU9QQgUmO/uGkh6wAtBb4yyDD/HM4hQPZfiE5AHNucIAtq5L/Tralw0kjyQG45T2k7AsV/8PAzfCbpLBokPnI8NryDQOIxgXwqYHJgex15f0KNgtkHggLMf5iYPr/l+G04Vu4+AZNSFMDl13UECc5AL8ysDKsfgmpe0plBqYs1OL8zbBM5zvD1McIt0SI/WCok/0CDhNYLgEVNRpstM0pJAcgyIVtDznBDs2W/U1yKgRrpJCYpgEJvIYn/Ayl97jBpiVK/WYAucf9Ai/Dyvc8DPX32MDisuz/KLQNv3ayAhDUhDn6gRlscrw4bWMYm/MVOP4zdD9BbSaBxEAp8t1/SMCd/gTJJdb8f7AZQTUxsgIQZHvrA0hZ2KgEKXuo5iIiDAIFFKgoQQfogYouTws+2QEI6mk8+AHp9oUK0TcVbn2LGXigwMEWqLQINGQzyQ5AkCFZNyBl4RSNH+AaENngkcKmKACR+7vGXCOzYU1RAIJSGazJAKoZRyKgOABXv4NkY1AtSI3unbcobWtNakcyxQH4j5EZngoJDTJc/wpp+uAKpGlKHxhAETGUAMUBCPIsLBWCWv74wNFPkNoTFEjhgpBeA0g96/8/DKDAA3UPYTU7PnMGkxxVAhCUCkFtM0IAuQEOqrlB/VZQf/WZFSTwQOUprGYnZNZgkadKAII8Q2wjNvQaLzywQSkRlGpBqc72LDe4CzZYAoZYd8Bn5UCTSnd/QMooYjWPZHWgESAQoFoKHKmBORqAFMb8aACOBiCFIUChdpQUiDxhTKG5w1o7LJw+/GH8z/jUnemgFNs/u2HtYxp47tFPZobeJ5ymTNI7/9l//csYQQM7hrWRe9+z5k269uUMAOSv9deZWI9wAAAAAElFTkSuQmCC')
		self.img_scroll_on = tk.PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAAAgCAYAAACFM/9sAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/E0XxQQoFRRS2iGIRQRTEUiKYJlokEYzabDYvIYnL7gYJtoKNRcBCtPFV+A+0FWwVBEERRKz8Ab4aCesdE0gQnWX2fpyZc5k5A55wzsjbzWOQLzhWJBTUFuNLWusLXgbxEaBXN2xzLjob49/xeUeTqrejqtf/+/4cHcmUbUBTm/CkYVqO8LRweN0xFW8L9xhZPSl8KByw5IDCV0pPVPlZcabK74qtWGQGPKqnlmngRAMbWSsvPCLsz+eKRu086iadqcJCVGq/zAFsIoQIopGgyCo5HEalFiSzv31jP7551sRjyN+khCWODFnxBkQtSteU1LToKflylFTuv/O00xPj1e6dQWh5ct23IWjdgUrZdb+OXLdyDN5HuCjU/WuS09SH6OW65j8A3yacXda1xC6cb0Hfg6lb+o/klelJp+H1FLri0H0D7cvVrGrrnNxDbEOe6Br29mFY9vtWvgEgR2gZpwP8dwAAAAlwSFlzAAAPYQAAD2EBqD+naQAAA79JREFUaAXtWc1rE0EUf5svmzYhjVoLtUKpIKmItEhFW1AoiIci6KFY/BNq8SJ4UbAXDyIqSu3RoyK9CIog4sGDrVi1KNL20lpsFKpiYk3StJt0zW/D7Eeym06STbHbPFh2dua9N/N+8+bNe4lAGfrY4+o/WJd6iHaV+BCQiG45ntBFQTpFlzIi1/nEqlw5CNwGgBkwq1QqAi4meGQyyJrVNwcCbzoiMpcCIL4WRQfF0gKH+NZm8TnVQ6sDkBe87cIqHfKJ1B1IKUhOx500l3TQbNJFvyWP0m/HhhYnHYDrGeuWUjS6/y9116cNWEWlr2F8p9K2e4MbQID3vSuq4HF1zkMTS3rx3h0i9TaoXqkw27ihR6CAoXf2xuTR+aRAXR8CJAr5ohNhoqHMs5XIwWtsX2PWswZmvIbg8eqxG1++G22Qhc3OFRrelzCJp0SF4ujPo7/kVTKeoeY/dH6PGoMx+DrqpL4pf8U3m9sDGa6XW1ZYs+T32WCMJg+rl9HooovuLbjlByGCl7AJj9siMniQgw7oAuGiY2GHV18pfEolgkR6Nuk01XHCH6cHB5blcSz2zCcfhdPbTPnNBjq9CXrWnpCHYezgrJ/WBP28dSRSnNxmKoh5INbRUiPR4EwNPYr4FH7tHE1j9RXxQrYGbg988bdO3mGsEouGB2H3sViHZJTWKPboGiOh7CYAvIG5+jzwwFwIPK0yrOPcZ68OPIy/T6gb2167qhWxvM0NIGYeCgeo461fji/4xjGBNy12RQjHcj0gQ55lGXzIXvlSi1dZBM/DxuZSrkfnjlv5XRSAmBjH9vR0UAYSMYfRcCgpA4m4ZEY9QTXQW1GtPI2onpY7Z8t4gPBovTGXx4rvogFkkwJIeGTjWFCOQawfRxulnhHtcmdrSC3wRnxW9CEM4Km0N5YMIDMSC0QAx24zuh+Ks6bt32UDyBDCbiMmgYxrZaIfYjZFyc3ZmI7N+LYMQBiPX2MKkbZ2RqpiBypscZEWsiQbVYARaQP6jVZ7HHNuAJFIw2uMUhVcGiin2NG9Nm98OyJesmOO2nqkNZp34UA/0p3NQty1cLYKWd8wADSxbJ7j4cJpW0jL5RdA7GtcMsSqYdxr2P+/dXJ7IKsxzQzA74O4ibUllRkvS8jNdG5EmmO2tmL7uWvhYhXbnb/oWtjugJRqH/cRLnUCu8tVASxzh6sAWgmg9g/jMvXaWpzhFE0JkvDtpONVk2ftmK0troBxX1ecdDPs7XTsfr52PJ4W+iswh61Vvoy4L9ydir37BwlUPNpyhxrVAAAAAElFTkSuQmCC')

		self.img_caps_off = tk.PhotoImage(data='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')
		self.img_num_off = tk.PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAAAgCAYAAACFM/9sAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/E0XxQQoFRRS2iGIRQRTEUiKYJlokEYzabDYvIYnL7gYJtoKNRcBCtPFV+A+0FWwVBEERRKz8Ab4aCesdE0gQnWX2fpyZc5k5A55wzsjbzWOQLzhWJBTUFuNLWusLXgbxEaBXN2xzLjob49/xeUeTqrejqtf/+/4cHcmUbUBTm/CkYVqO8LRweN0xFW8L9xhZPSl8KByw5IDCV0pPVPlZcabK74qtWGQGPKqnlmngRAMbWSsvPCLsz+eKRu086iadqcJCVGq/zAFsIoQIopGgyCo5HEalFiSzv31jP7551sRjyN+khCWODFnxBkQtSteU1LToKflylFTuv/O00xPj1e6dQWh5ct23IWjdgUrZdb+OXLdyDN5HuCjU/WuS09SH6OW65j8A3yacXda1xC6cb0Hfg6lb+o/klelJp+H1FLri0H0D7cvVrGrrnNxDbEOe6Br29mFY9vtWvgEgR2gZpwP8dwAAAAlwSFlzAAAPYQAAD2EBqD+naQAAArZJREFUaAXtms2KwjAQx+MqfqDgQVAUFBQ8ePCke93X2H2Jve5b7L7TgldB8OhNQVDwICgoKLv5Z3dKWmttm1RrbaCYpjPJzK+TZEJljJdCofDGf37iyxODT7BD+eBXDM8fg6/EPzyAjIsPAinS6fV6VI1/XRAYDodCygCIu3Q6zZLJpAv1xxY5Ho8GABNAJ3jT6dRQajQaRt1aITknGavOvd3LnEwAnRwhMJDJZrOsXC7bipNclAHKjj/JN27rBMmtfJTlfAHc7XZsuVxGmYtr3zwDrFQqovP5fO56kCgLul4DCQLWvsViwTabDVuv16xYLNKji7/j8djQ6Xa7tvJOMvQMuqvViskvsdPpsHw+z0ajETscDqJvrNX9ft92HF2NniMQwPjRT4x/q7UQLw7wZFuwpEwmE2EXzRIsNTJkXdDkfjwDhHKtVhN9wBFc1y4ED5HYbDZNtrTbbYarVCqJdkAMsvgCiGmM6YES9Bu2cx5T1JomoQ0RSeAwnVG2261dF9rafAHE6JQHYi0K+i1bvQUoXNZihWp9HsS9b4AwNpX624Nms1kQtp3t0w4ehM+1n+1IwwPfADE2rYXYla8dhRp819KFEkB5yjxqYq0EEK+QUoZbbCZaQkixE2WA9XpdmIBdUEcUBr1rKvI6UVcGiHSGovBSYk2pzzlI8inixNKQNigDhF8UhZc2EtolEa10aoA+gAIejoe0s6P9Horns7CdU4gswLl0KkHuiCgFaOzcyCEBjMAjkjOZjJCxGyeMbVoiEI7JO7KTozj0y5EIeIDYarXEEcxJN4zPjK9y+KiUy+XCaGMobRoMBsIubREYSi+vYFQMUBFyDDAGqEhAUd0UgfIHY8V+I61OnHj28JPgedf3fr9/ibTHATiH3JcfIJ5F1/xL+yuvxP/Q8sCgWq2+A94vHNHJFu2sc/YAAAAASUVORK5CYII=')
		self.img_scroll_off = tk.PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAAAgCAYAAACFM/9sAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/E0XxQQoFRRS2iGIRQRTEUiKYJlokEYzabDYvIYnL7gYJtoKNRcBCtPFV+A+0FWwVBEERRKz8Ab4aCesdE0gQnWX2fpyZc5k5A55wzsjbzWOQLzhWJBTUFuNLWusLXgbxEaBXN2xzLjob49/xeUeTqrejqtf/+/4cHcmUbUBTm/CkYVqO8LRweN0xFW8L9xhZPSl8KByw5IDCV0pPVPlZcabK74qtWGQGPKqnlmngRAMbWSsvPCLsz+eKRu086iadqcJCVGq/zAFsIoQIopGgyCo5HEalFiSzv31jP7551sRjyN+khCWODFnxBkQtSteU1LToKflylFTuv/O00xPj1e6dQWh5ct23IWjdgUrZdb+OXLdyDN5HuCjU/WuS09SH6OW65j8A3yacXda1xC6cb0Hfg6lb+o/klelJp+H1FLri0H0D7cvVrGrrnNxDbEOe6Br29mFY9vtWvgEgR2gZpwP8dwAAAAlwSFlzAAAPYQAAD2EBqD+naQAAAzdJREFUaAXtmstqIkEUQCuj+MCAC8GgoAtB0UVAkNnJ/MbMT8x2/mLmnwZcuFAUXAQiJGBAUHAhKCgYMn2auU3Ztlq+krGnLzRV6Xrde+reerRRypLb29tvVvIWPAcx+Ak75If1BPCOY/Dr5i88QAZyBIGwtKnVapINUgMC7XbbruUA5K9IJKJCoZBB8/+7yuvrqwNgDaApvMlkoqbTqZrP505HsVhMRaNRlUgkVCqVct77MaNzWgO4z1iAPTw8qMVisVEVoCL1el2yvk+NAQKv0+k4QPAyvE0Xt1fqZX7NGwPs9/s2g3A4rO7v7zfg+RXQPrs+7asg5bPZzM5ms9kAnkCxUmMP1NqcJTsej9VgMPBcTxlg1zraaDRsHaROr9ezNzVdMTa1SqVy8ck29kBRDsNPFZaDx8dHB551lVTJZNJ+WCJMBV1arZYNj3b0QV8IG50sO6b9HVPPWFtCdzgc2oo1m01VKBRUOp0+eEy8bjQa2e0wtlwuK7xFF31H19+7809PT2q1Wqm7uztVLBadYsbgYdlh83Nvdk7FM2SMPRBgzDCC0ngQs78rDL30YxIQ4FWr1Q14lMk45HcJejCxOjzq6xPLmfWSYgwQJdh9S6WSYzRhAkBAEi5e50NdeeBhNJLL5fSio/J4HhPrFrdHu8vP+bdxCMugzC4P6w+hKOFGngfAugdIO1KpS/4ct5Vt49A/k41wO7qkHAxQlBGQeN3Ly4uzrhHaXHW8AIn3mYaojHVM+h5joNdBIexlCOHCGiQzTp3n52evqr58dzJAocKMsyYh29ZCOaLooSztrzU9G0AA7Ftv9OOEXyCeFaAcsrftgvqi75cwNwbIoRWv8QpPzlpcp6RMB6WHJmAlzDnkdrtd5T6n0YecFfW2/2reeBfGKBPDAJTP57fay4YDJCYDiHxf9BIOyNcgxgC5OcgXGS/DOLZgtMnxgR2bcGdCvPo06cNLh4945/wqx49K8Xj8I3S4yjHli5DxGniVVr6D0gHAEyEHAAOAJxI4sfmaB+o/GJ/Yr6+bCyfravp2Y12/fi+Xyy++tvgCxnEpsL5pfra7tj4/fbUywX9oHcAgk8l8B94fcBET7/iHxxQAAAAASUVORK5CYII=')
		self.disabled_img = tk.PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAFAAAAAgCAYAAACFM/9sAAABb2lDQ1BpY2MAACiRdZE7SwNBFIU/E0XxQQoFRRS2iGIRQRTEUiKYJlokEYzabDYvIYnL7gYJtoKNRcBCtPFV+A+0FWwVBEERRKz8Ab4aCesdE0gQnWX2fpyZc5k5A55wzsjbzWOQLzhWJBTUFuNLWusLXgbxEaBXN2xzLjob49/xeUeTqrejqtf/+/4cHcmUbUBTm/CkYVqO8LRweN0xFW8L9xhZPSl8KByw5IDCV0pPVPlZcabK74qtWGQGPKqnlmngRAMbWSsvPCLsz+eKRu086iadqcJCVGq/zAFsIoQIopGgyCo5HEalFiSzv31jP7551sRjyN+khCWODFnxBkQtSteU1LToKflylFTuv/O00xPj1e6dQWh5ct23IWjdgUrZdb+OXLdyDN5HuCjU/WuS09SH6OW65j8A3yacXda1xC6cb0Hfg6lb+o/klelJp+H1FLri0H0D7cvVrGrrnNxDbEOe6Br29mFY9vtWvgEgR2gZpwP8dwAAAAlwSFlzAAAPYQAAD2EBqD+naQAAAUFJREFUaAXt2k0KglAUBWBN8QfcgANXIc2kbdQmmraL2lPg1AU5kHpPUp7KvRzfKPAI4vXe86I+bJAWBGYriuJmDh/uuwye1s5uD7MTz8/gFf7wLCQ3D4F4WlPX9VTyCAh0XTemZkB7liRJEEURsPzYkWEYZoDTXJmCeK6GXLtOC0B5CSeSAAElGbBPQBBKihFQkgH7BAShpBgBJRmwT0AQSooRUJIB+wQEoaTY4qecFHL7bdu6p5u6aZpNb934l9dYvy+fc16BPmrOmvl2lr0bk+e5M2KpCUzfIl6BmhIwIyCApEUIqOkAMwICSFqEgJoOMCMggKRFCKjpADMCAkhahICaDjAjIICkRQio6QCzBaD7wBhYe9jI5BTH8SdM0/Td9/3lsBqeHzzLsqCqqvO43Dxpv5qC/9DaYVCW5d3ifQE1cwhKfsJuigAAAABJRU5ErkJggg==')

		self.overrideredirect(True)
		self.lock_bar = tk.Frame(self, bg='black')
		self.lock_bar.pack()

		self.btn_close = tk.Button(self.lock_bar,
		text='X', 
		command= self.__close,
		bg = "#000000", 
		activebackground='red',
		font="bold",
		fg='#777777',
		border=0)

		self.capslbl = tk.Label(self.lock_bar, 
		image=self.img_caps_off ,
		bg = "black")

		self.numlbl = tk.Label(self.lock_bar,
		image=self.img_caps_off ,
		bg = "black")		

		self.scrlbl = tk.Label(self.lock_bar,
		image=self.img_caps_off ,
		bg = "black")
		
		self.capslbl.pack(side = "left")
		self.numlbl.pack(side = "left")
		self.scrlbl.pack(side = "left")
		self.btn_close.pack(side = "right")
		

		#set up window
		self.resizable(False, False)
		self.attributes("-topmost" , True)
		self.bind("<ButtonPress-1>", self.__start_window)
		self.bind("<B1-Motion>", self.__move_window)
		self.update()

		self.timer = RepeatTimer(self.interval, self.flash)
		self.timer.daemon = True
		self.timer.start()
		
				
	def set_locks(self, caps, num, scroll):
		'''
		Updates flashing images according to recieved lock status
		'''
		self.caps_on = caps
		self.num_on = num
		self.scroll_on = scroll
		
        

	def get_coords(self):
		'''
		Returns pixel position of window
		'''
		coords = []
		coords.append(self.winfo_rootx())
		coords.append(self.winfo_rooty())
		return coords


	def flash(self):
		'''
		Flashes on-screen lock lights. 
		'''
		try:
			if self.show_on_img:
				self.show_on_img = False
				
				self.capslbl.configure(image=self.img_caps_off)
				self.capslbl.image = self.img_caps_off
				self.numlbl.configure(image=self.img_num_off)
				self.numlbl.image = self.img_caps_off
				self.scrlbl.configure(image=self.img_scroll_off)
				self.scrlbl.image = self.img_caps_off


				if self.ignore_caps:
						self.capslbl.configure(image=self.disabled_img)
						self.capslbl.image = self.disabled_img	

				if self.ignore_num:
						self.numlbl.configure(image=self.disabled_img)
						self.numlbl.image = self.disabled_img

				if self.ignore_scroll:
						self.scrlbl.configure(image=self.disabled_img)
						self.scrlbl.image = self.disabled_img
			else:
				self.show_on_img = True

				if self.caps_on == True and self.ignore_caps == False:
					self.capslbl.configure(image=self.img_caps_on)
					self.capslbl.image = self.img_caps_on

				if self.num_on == True and self.ignore_num == False:
					self.numlbl.configure(image=self.img_num_on)
					self.numlbl.image = self.img_num_on

				if self.scroll_on == True and self.ignore_scroll == False:
					self.scrlbl.configure(image=self.img_scroll_on)
					self.scrlbl.image = self.img_scroll_on
		except: # incorrect behavior will be obvious & not app-breaking
			return

			
	def show_light(self, name):
		'''
		Restores a disabled indicator
		'''
		if name == "caps":
			self.ignore_caps = False
			self.capslbl.configure(image=self.img_caps_on)
			self.capslbl.image = self.img_caps_on

		elif name == "num":
			self.ignore_num = False
			self.numlbl.configure(image=self.img_num_on)
			self.numlbl.image = self.img_num_on

		elif name == "scroll":
			self.ignore_scroll = False
			self.scrlbl.configure(image=self.img_scroll_on)
			self.scrlbl.image = self.img_scroll_on

		
		
	def hide_light(self, name): # for those with num lock on all the time
		'''
		Disables an indicator
		'''
		name = name.lower()
		if name == "caps":
			self.ignore_caps = True
			self.capslbl.configure(image=self.disabled_img)
			self.capslbl.image = self.disabled_img

		elif name == "num":
			self.ignore_num = True
			self.numlbl.configure(image=self.disabled_img)
			self.numlbl.image = self.disabled_img

		elif name == "scroll":
			self.ignore_scroll = True
			self.scrlbl.configure(image=self.disabled_img)
			self.scrlbl.image = self.disabled_img
		else:
			return



	def __start_window(self, event):
		'''
		Allows window to be moved
		'''
		self.x = event.x
		self.y = event.y
		
		

	def __move_window(self, event):
		'''
		Moves window with mouse, accounting for offset
		'''

		deltax = event.x - self.x
		deltay = event.y - self.y

		x = self.winfo_x() + deltax
		y = self.winfo_y() + deltay
		self.geometry(f"+{x}+{y}")
		

	def __close(self):
		'''
		Destroying the window will cause issues with settings when 
		it tries to find this and save its coordinates
		'''
		self.withdraw()
















################################################################### CLASS SEPERATION























# class poached from stack exchange, I don't know about python threading. 
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)



















################################################################### CLASS SEPERATION
























class settingsFrame(tk.Frame):
	'''
	First frame in application
	'''
	def __init__(self, root, settings):
		super().__init__()
		self.settings = settings


		self.fm_settings = tk.Frame(root, background=self.settings.bg_color)
		self.fm_settings.grid(row=0, column=0, padx=0, pady=0, sticky= "n")
	

		self.btn_mk_adv = tk.Button(self.fm_settings,
		text = "Advanced",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)
		self.btn_mk_adv.grid(row = 3, column = 0, sticky = "w")

		# bug: when pressing advanced button, this checkbox unchecks
		# however, the proper value is kept: visual bug only. 
		# checked becomes false, unchecked = true 
		self.chk_mute = tk.Checkbutton(self.fm_settings,
		text="Mute",
		background=self.settings.bg_color)

		self.chk_mute.grid(row=2, column = 0, sticky = "w" )
		
		# the assumption is pygame volume, so the max is multiplied by 100
		self.slider_vol = tk.Scale(self.fm_settings, 
		from_= self.settings.min_vol,
		to= self.settings.max_vol * 100,
		orient = tk.HORIZONTAL,
		background=self.settings.bg_color, 
		foreground= self.settings.reg_text_color,
		borderwidth=0,
		relief="flat")
		self.slider_vol.grid(column = 0 , row = 1)
		
		
		self.lbl_key_name = tk.Label(self.fm_settings,
		text="Key: ",
		font=(self.settings.title_font, self.settings.title_size),
		bg=self.settings.bg_color,
		fg= self.settings.high_text_color)
		self.lbl_key_name.grid(column = 0, row = 0, sticky = "w")


		self.__set_defaults()


			

	def display_key(self, old_key):
		self.lbl_key_name.config(text = str("Key: " + old_key))
		
	
	def __set_defaults(self):
		'''
		Sets elements to their values in settings, then binds them. 
		'''
		self.slider_vol.set(self.settings.vol_settings["curr_vol"] * 100)
		
		if self.settings.vol_settings["muted"] == True:
			self.chk_mute.select()
		else:
			self.chk_mute.deselect()

		
		self.slider_vol.configure(command = self.settings.set_vol)
		self.chk_mute.configure(command = self.settings.toggle_mute)
		self.btn_mk_adv.configure(command = self.settings.mk_advanced_settings)
















################################################################### CLASS SEPERATION























class profilesFrame(tk.Frame):
	'''
	Second frame, shows what files were found to user
	'''
	def __init__(self, root, settings):
		super().__init__()

		self.settings = settings
		self.fm_profiles = tk.Frame(root, background=self.settings.bg_color)
		self.fm_profiles.grid(row=0, column=1, padx=8, pady=0, sticky= "n")

		
		self.listbox_pf = tk.Listbox(self.fm_profiles,
		height=6,
		background= self.settings.dk_color,
		foreground=self.settings.reg_text_color)
		self.listbox_pf.grid(column=0,	row=1, sticky='nwes')

		self.lbl_pf = tk.Label(self.fm_profiles,
		text = "Profiles",
		font=(self.settings.title_font, self.settings.title_size),
		bg=self.settings.bg_color,
		fg= self.settings.high_text_color)
		self.lbl_pf.grid(column=0, row=0, sticky="n")


		self.bind_widgets()




	def set_label(self, text):
		if text == "":
			text = "(Nothing Selected)"
		self.lbl_pf.configure(text =  text )
			
		
	def update(self, profiles):
		profiles.sort()
		for profile in profiles:
			self.listbox_pf.insert("end", str(profile))
		
	
	def bind_widgets(self):
		self.listbox_pf.bind('<<ListboxSelect>>', self.settings.load_pf)


	def get_selected(self):
		sel = ""
		try:
			sel = self.listbox_pf.get(self.listbox_pf.curselection())
		except:
			self = self.listbox_pf.get(0)
		return sel


	def sel_in_list(self, name):
		'''
		Selects a specific element from the listbox.
		Used to auto-load user's chosen sound profile.
		'''
		index = 0
		for i, listbox_entry in enumerate(self.listbox_pf.get(0, tk.END)):
			if listbox_entry == name:
				index = i
				
		self.listbox_pf.select_set(index)
		self.listbox_pf.event_generate("<<ListboxSelect>>")
		self.listbox_pf.update_idletasks()

	


















################################################################### CLASS SEPERATION
























class keypersFrame(tk.Frame):
	'''
	Third frame, shows what keypers were found and options.
	'''
	def __init__(self, root, settings):
		super().__init__()

		self.settings = settings
		self.fm_keypers = tk.Frame(root, background=self.settings.bg_color)
		self.fm_keypers.grid(row=0, column=3, padx=8, pady=0,sticky= "n")

		self.popup= None
		self.warn_popup = None
		# row 0
		self.lbl_title = tk.Label(self.fm_keypers,
		text = "Keypers",
		font=(self.settings.title_font, self.settings.title_size), 
		bg=self.settings.bg_color,
		fg= self.settings.high_text_color)
		self.lbl_title.grid(column=0, row=0, sticky="W", columnspan=4)

		# row 1
		self.btn_del_ky = tk.Button(self.fm_keypers,
		text = "x",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)

		self.btn_del_ky.grid(row = 1, column = 0, sticky = "w")

		self.btn_add_ky = tk.Button(self.fm_keypers,
		text = "+",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)

		self.btn_add_ky.grid(row = 1, column = 1, sticky = "w")

		self.btn_rnm_key = tk.Button(self.fm_keypers,
		text = "Rename",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)

		self.btn_rnm_key.grid(row = 1, column = 2, sticky = "w")

		self.btn_wipe_ky = tk.Button(self.fm_keypers,
		text = "Wipe",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)
		self.btn_wipe_ky.grid(row = 1, column = 3, sticky = "w")

		# row 2
		self.ky_listbox = tk.Listbox(self.fm_keypers, 
		height=6,
		background= self.settings.dk_color, 
		foreground=self.settings.reg_text_color)
		self.ky_listbox.grid(column=0,	row=2, sticky='w', columnspan=4)


		self.bind_widgets()


		self.settings.kyhive.load(self.settings.defaults["keyper"])
		self.sel_in_list(self.settings.defaults["keyper"])
	

	def set_current(self, text):
		if text == "":
			text = "(None)"

		self.lbl_title.configure(text = text)

	
	def update(self, data):
		self.ky_listbox.delete(0,tk.END)
		for element in data:
			self.ky_listbox.insert("end", str(element))

	
	def bind_widgets(self):
		self.ky_listbox.bind('<<ListboxSelect>>', self.settings.load_ky)	
		self.btn_add_ky.configure(command = self.__mk_new_popup)
		self.btn_del_ky.configure(command = self.__mk_warn_popup)
		self.btn_rnm_key.configure(command = self.__mk_rename_popup)
		self.btn_wipe_ky.configure(command = self.settings.wipe_key_data)


	def get_selected(self):
		sel = ""
		try:
			sel = self.ky_listbox.get(self.ky_listbox.curselection())
		except:
			sel == "total"
		return sel

	def sel_in_list(self, name):
		'''
		Selects a specific element from the listbox.
		Used to auto-load user's chosen keyper.
		'''

		index = 0
		for i, listbox_entry in enumerate(self.ky_listbox.get(0, tk.END)):
			if listbox_entry == name:
				index = i

		self.ky_listbox.select_set(index)
		self.ky_listbox.event_generate("<<ListboxSelect>>")
		self.ky_listbox.update_idletasks()


# update to single class with 'type' option
	def __mk_rename_popup(self):
		self.popup = entry_popup(self.fm_keypers, "Rename Keyper")
		self.popup.bind_entry(self.del_rename_popup)
		x = self.ky_listbox.winfo_rootx()
		y = self.ky_listbox.winfo_rooty()
		self.popup.geometry("+%d+%d" %(x, y))

	def __mk_new_popup(self):
		self.popup = entry_popup(self.fm_keypers, "Add Keyper")
		self.popup.bind_entry(self.del_add_popup)
		window_geometry = str(self.popup.winfo_width()) + 'x' + str(self.popup.winfo_height() ) + '+' + str(self.ky_listbox.winfo_x()) + '+' + str(self.ky_listbox.winfo_y()) #Creates a geometric string argument
		x = self.ky_listbox.winfo_rootx()
		y = self.ky_listbox.winfo_rooty()
		self.popup.geometry("+%d+%d" %(x, y))

	def del_rename_popup(self, lol):
		if self.popup != None:
			string = self.popup.entry.get()
			self.settings.rnm_ky(string)
			self.popup.destroy()

	def del_add_popup(self, lol):
		if self.popup != None:
			string = self.popup.entry.get()
			self.settings.add_ky(string)
			self.popup.destroy()

	def __mk_warn_popup(self):
		self.warn_popup = warn_popup(self.fm_keypers, str("Delete Keyper?"))
		self.warn_popup.bind_yes(self.del_warn_popup)
		x = self.ky_listbox.winfo_rootx()
		y = self.ky_listbox.winfo_rooty()
		self.warn_popup.geometry("+%d+%d" %(x, y))

	def del_warn_popup(self):
		if self.warn_popup != None:
			self.settings.del_ky()
			self.warn_popup.destroy()











################################################################### CLASS SEPERATION









class entry_popup(tk.Toplevel):
	'''
	Prompts for entering a string
	'''
	def __init__(self, window, title):
		super().__init__(window)
		self.title(title)
		self.grab_set() 

		self.entry = tk.Entry(self,text = "name...")
		self.entry.grid(row = 0, column = 2, sticky = "w")

	def bind_entry(self, command):
		self.entry.bind('<Return>', command)








################################################################### CLASS SEPERATION









class warn_popup(tk.Toplevel):
	'''
	Warns before confirming an action
	'''
	def __init__(self, window, warning):
		super().__init__(window)
		self.title("Caution")
		self.grab_set() 

		self.lbl_warn = tk.Label(self,text = warning)
		self.lbl_warn.grid(row = 0 , column=1)

		self.btn_yes = tk.Button(self,text = "Yes")
		self.btn_yes.grid(row = 1, column = 0, sticky = "w")

		self.btn_no = tk.Button(self,text = "No", command = self.destroy)
		self.btn_no.grid(row = 1, column = 1, sticky = "w")

	def bind_yes(self, command):
		self.btn_yes.configure(command= command)










################################################################### CLASS SEPERATION
















class kydetailsFrame(tk.Frame):
	'''
	Fourth frame, shows relevent stats about keyper
	'''

	def __init__(self, root, settings):
		super().__init__()

		self.root = root
		self.settings = settings
		self.edit_pnl = None

		self.fm_keypers = tk.Frame(root, background=self.settings.bg_color)
		self.fm_keypers.grid(row=0, column=4, sticky= "n")


		# row 0
		self.lbl_total = tk.Label(self.fm_keypers, 
		text = "Total: ",
		font=(self.settings.title_font, self.settings.title_size), 
		bg=self.settings.bg_color,
		fg= self.settings.high_text_color)
		self.lbl_total.grid(column=0, row=0, sticky="w")

		# row 1
		self.lbl_most = tk.Label(self.fm_keypers, 
		text = "Most: ",
		font=(self.settings.title_font, self.settings.title_size), 
		bg=self.settings.bg_color,
		fg= self.settings.high_text_color)
		self.lbl_most.grid(column=0, row=1, sticky="w")
		
		# row 2
		self.lbl_least = tk.Label(self.fm_keypers, 
		text = "Least: ",
		font=(self.settings.title_font, self.settings.title_size), 
		bg=self.settings.bg_color,
		fg= self.settings.high_text_color)
		self.lbl_least.grid(column=0, row=2, sticky="w")
		
		# row 3
		self.listbox_keys = tk.Listbox(self.fm_keypers, height=6)
		self.listbox_keys.grid(column=0,	row=3, sticky='nwes')

		self.scrollbar = tk.Scrollbar(self.fm_keypers, orient="vertical")
		self.scrollbar.grid(column = 1, row = 3, sticky = "nwes" )

		self.listbox_keys.configure(
		yscrollcommand=self.scrollbar.set,
		background= self.settings.bg_color, 
		foreground=self.settings.reg_text_color)
		self.listbox_keys.bindtags((self.listbox_keys, self.fm_keypers, "all"))
		
		self.scrollbar.config(
		command=self.listbox_keys.yview,
		background=self.settings.dk_color)


	def update(self, keys):
		keys.sort()
		self.listbox_keys.delete(0,tk.END)
		for key in keys:
			self.listbox_keys.insert("end", str(key))

	
	def set_stats(self, least , most, total):
		self.lbl_least.configure(text = "Least: " + least)
		self.lbl_most.configure(text = "Most: " + most)
		self.lbl_total.configure(text = "Total: " + total)



















################################################################### CLASS SEPERATION
























class adv_settings(tk.Toplevel):
	'''
	Settings popup for fine tuning application
	'''
	def __init__(self, window, settings):
		super().__init__(window)
		self.title("Settings")
		self.root = window
		self.settings = settings 
		self.grab_set() 
		self.settings.mod_keys = True;
		self.configure( background=self.settings.fg_color)


		# row 0
		self.btn_reset_lockbar = tk.Button(self,
		text = "Reset Lock Light bar",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)
		self.btn_reset_lockbar.grid(column = 0, row = 0, padx= 4, pady = 4)

		self.chk_repeat = tk.Checkbutton(self, 
		text="Repeat Sound when holding key: ",
		background=self.settings.fg_color)
		self.chk_repeat.grid(column = 1,  row= 0)


		# row 1
		#chkboxes needs to be configured before grid, or the value is incorrect. 
		self.capbool = tk.BooleanVar()

		self.chk_caps = tk.Checkbutton(self, 
		text="Caps " , variable = self.capbool,
		background=self.settings.fg_color)
		self.chk_caps.configure(command = 
		lambda: self.settings.show_lock_light("caps", self.capbool.get()))
		self.chk_caps.grid(column = 0,  row= 1, sticky="w")


		self.numbool = tk.BooleanVar()

		self.chk_num = tk.Checkbutton(self, 
		text="Num " , variable = self.numbool,
		background=self.settings.fg_color)

		self.chk_num.configure(command = 
		lambda: self.settings.show_lock_light("num", self.numbool.get()))
		self.chk_num.grid(column = 1,  row= 1, sticky="w")
		
		
		self.scrbool = tk.BooleanVar()

		self.chk_scroll = tk.Checkbutton(self, 
		text="Scroll " , 
		variable = self.scrbool,
		background=self.settings.fg_color)

		self.chk_scroll.configure(command = 
		lambda: self.settings.show_lock_light("scroll", self.scrbool.get()))
		self.chk_scroll.grid(column = 2,  row= 1, sticky="w")
		
		

		
		# row 4
		self.lbl_key = tk.Label(self, 
		text = "Keys:", 
		background=self.settings.fg_color,
		foreground= self.settings.high_text_color)
		self.lbl_key.grid(column = 1, row = 4)


		self.mute_keys = tk.IntVar()
		self.radio_mute = tk.Radiobutton(self, 
		text="Silence",
		padx = 20, 
		variable=self.mute_keys, 
		value = 1, background=self.settings.fg_color)
		self.radio_mute.grid(column = 0, row = 4)


		# row 5
		self.loud_radio = tk.Radiobutton(self, 
		text="Unmute",
		padx = 20, 
		variable=self.mute_keys, 
		value = 0,
		background=self.settings.fg_color)
		self.loud_radio.grid(column = 0, row = 5)


		self.btn_clear_keys = tk.Button(self,
		text = "Clear",
		background = self.settings.bg_color,
		foreground= self.settings.reg_text_color)
		self.btn_clear_keys.grid(column = 2, row = 5, sticky="w")


		self.__set_default()		
		
	
		


	def __set_default(self):

		if self.settings.ind_settings["caps"] == True:
			self.chk_caps.select()
		else:
			self.chk_caps.deselect()

		if self.settings.ind_settings["num"] == True:
			self.chk_num.select()
		else:
			self.chk_num.deselect()		

		if self.settings.ind_settings["scroll"] == True:
			self.chk_scroll.select()
		else:
			self.chk_scroll.deselect()

		if self.settings.vol_settings["rpt_protection"] == True:
			self.chk_repeat.deselect()
		else:
			self.chk_repeat.select()	

		self.bind("<ButtonPress-1>", self.__start_window)
		self.bind("<B1-Motion>", self.__move_window)

		self.btn_reset_lockbar.configure(command= self.settings.reset_lockbar)
		self.chk_repeat.configure(command= self.settings.toggle_rpt_prot)
		self.btn_clear_keys.configure(command= self.settings.clear_muted_keys)

		self.radio_mute.configure(command= lambda: 
		self.settings.toggle_debeep(True))

		self.loud_radio.configure(command= lambda:
		self.settings.toggle_debeep(False))

		
	
	def update_muted_keys(self,keys):
		'''
		Updates label with keys that wont make sounds on press
		'''
		if len(keys) != 0:
			keys = list(keys)
			keys.sort()
			keys = str(keys)
			self.lbl_key.config(text= keys)
		else:
			self.lbl_key.config(text= "(None)")
		return
		
	def __start_window(self, event):
		'''
		Allows window to be moved
		'''

		self.x = event.x
		self.y = event.y
		

	def __move_window(self, event):
		'''
		Moves window with mouse, accounting for offset
		'''

		deltax = event.x - self.x
		deltay = event.y - self.y

		x = self.winfo_x() + deltax
		y = self.winfo_y() + deltay

		self.geometry(f"+{x}+{y}")		

	
	def __close(self):
		self.settings.mod_keys = False
		self.settings.key_silencing = False
		self.destroy()
	
