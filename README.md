# auction site

## User account
- [x] login (email used for communication and notifications)
- [x] password
- [x] user name (presented on the account profile)
- [x] city
- [x] address (street, house number, ZIP code)
- [x] account creation date
- [x] account status (ACTIVE / INACTIVE / BLOCKED)
- [x] logotype / thumbnail / avatar
- [x] type (NORMAL/PREMIUM)

##Auction details
- [x] title
- [x] description
- [x] photos (optional)
- [x] category
- [x] minimum amount to pay
- [x] Buy Now amount ( it disappears if an auction has started) 
- [x] promoted (it can be assumed, that a premium account can promote e.g. 10 auctions a month)
- [x] location (corresponds to the location of the user account)
- [x] auction start date
- [x] auction end date
- [x] number of visits (page views) 

  ##Bidding
- [x] auction
- [x] user
- [x] amount to pay

 ##Purchase (the highest bid or Buy now)
- [x] auction
- [x] user
- [x] amount to pay

 ##Auction observation
- [x] auction
- [x] user

##Transaction (purchase) assessment
- [ ] purchase
- [ ] seller rating
- [ ] seller’s comment
- [ ] buyer’s rating
- [ ] buyer's comment

##Main page presentation
- [x] presentation of categories(main - if their structure is tree-like): e.g. a list of links in the left or right column, leading to auctions from the selected category
- [x] presentation of a list of recently added auctions (e.g. 10)
- [x] presentation of a list of ending auctions (e.g. 10)
- [x] presentation of a list of auctions of a currently logged in user
- [x] presentation of a list of auctions, that a logged in user is bidding on
- [x] presentation of a list of observed auctions
- [x] presentation of a list of "just ended" auctions (e.g. 10)
- [ ] (optional) additional auction lists, e.g. the most popular (most visits or auctions)

##Auction category selection
- [x] a list of categories, in which auctions are placed 

##User account management
- [x] form to set up an account
- [x] page (available after logging in) for editing account details
- [ ] just like on the main page, there should appear lists of auctions: observed, started, auctioned (also lost) and completed (won as well as those which did not receive the minimum amount)

##Auction start
- [x] a form for starting the auction and determining its parameters
- [x] an auction can be cancelled (if there was no bid)

##Auction search
- [x] page presenting auction search results, e.g. category links from the main page lead to it
- [x] whenever the category name is presented, it should be clickable and lead to a page with results presentation
- [ ] additionally, on the results page, you can limit / filter auctions (e.g. by city) and sort, e.g. by the date of adding, after the date of the end of the auction
- [x] the mechanism must take into account premium auctions and presents them first
- [ ] (optional) a field for entering an auction number or account name: search by number (presents a specific auction), search for a user's auction (presents a list of their auctions)

##Bid and buy
- [x] a logged in user can bid on an auction
- [x] can input any amount to pay
- [x] can immediately choose Buy now
- [x] can only bid on ongoing auctions
- [x] the highest bid or Buy now becomes Purchase
- [ ] if the minimum amount has not been reached, there is no winner
- [ ] Warning! For simplicity, you need to write a mechanism, that will be triggered each time you enter the site and will "close" auctions, that have ended (since the last visit to the site) and will select winners
- [ ] (optional) with the help of a trainer you can try to use Celery

##Transaction Ratings
- [ ] both the seller and the buyer can leave a rating and a comment

##Auction observation
- [x] logged in user can add auction to the watch list
- [x] after entering the observed auction, this fact should be marked, e.g. with an inscription or a star image

##Project development
- [ ] in its current form, the design is quite complicated
- [ ] developing the functionality is left to the Student (inspired by existing websites and own ideas)

##Additional requirements
- [ ] it is necessary to ensure an aesthetic and functional data presentation
- [ ] data collected from users should be pre-validated
