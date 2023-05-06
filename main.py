from scraper import NitterSearch

def main():
    NitterSearch(query='a pizza ontem estava', 
    			 random_time=True, 
    			 random_interval=(0.001, 0.01))

if __name__ == "__main__":
	main()