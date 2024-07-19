# GDSC Hanyang 23-24 mini project
## Backend_server part
### STACK : Flask, Python, MySQL, AWS
<br>   
   
## Table   


| HTTP methods | 기능,의미 |	소스 파일 |	Return | Request |
| /login | POST | 로그인(ID와 password 받아서) |	app/login.py | 로그인정보-json,200	ID Password | |

| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |


<br>   
	

/signup	POST	회원가입(DB-’고객’테이블에 저장)	app/login.py	로그인성공메시지→json, 201	ID
username 
residence_area 
password 
/logout	POST	로그아웃, 단순히 인증세션에서 logout	app/login.py	로그아웃성공메시지→json, 200	X
/products	GET	(로그인 유저의 지역과 일치하는 지역의) 판매상품 (정보포함된) 리스트 전달	app/product.py	DB정보 모두 포함된 상품들의 정보→json	
/products/int:product_id	GET	상품리스트에서 특정 상품을 클릭할때,  해당하는 상품_detail 페이지로 이동하는 과정
⇒ 해당 판매상품의 정보를 전달.	app/product.py	해당 상품의 정보→ json	
/products/int:product_id/join_group	POST	해당 상품의 그룹참여 버튼을 누르면 해당 그룹이 (현재 로그인된)유저세션의 ‘장바구니’에 담김.	app/product.py	해당 그룹의 id만 json	group_id : INT
/cart	GET	장바구니 페이지 접속시에 유저의 그룹들에 대한 정보 전달( 해당 공동 구매 그룹의 상품이름, 마켓이름, 그룹의 size..)	app/cart.py	그룹들에 대한 정보→ json	
/cart/<int:group_id>/purchase	POST	장바구니 페이지에서 최종 구매버튼 클릭
-  group id,구매수량을 전달 받고, DB의 그룹, Order 테이블 업데이트
- 그리고 장바구니에서 구매참여한 그룹 제거.	app/cart.py	구매 성공→json, 200	group_id : INT
구매 수량: INT
					
