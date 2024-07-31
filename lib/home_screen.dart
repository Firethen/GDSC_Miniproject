import 'package:flutter/material.dart';
import 'mycart.dart';
import 'recommend.dart';
import 'product_detail.dart';
import 'api_service.dart';

class HomeScreen extends StatefulWidget {
  final Color customBlue;
  final String? dongName;
  final int userId;

  HomeScreen({required this.customBlue, required this.dongName, required this.userId});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Map<String, dynamic>>> recommendedProductsFuture;
  late Future<List<Map<String, dynamic>>> allProductsFuture;

  final List<Map<String, String>> recentlyViewedProducts = List.generate(
    4,
        (index) => {
      'image': 'assets/images/apple.jpg',
      'description': '아삭한 사과칩',
    },
  );

  final ApiService apiService = ApiService();

  @override
  void initState() {
    super.initState();
    recommendedProductsFuture = apiService.fetchRecommendedProducts(widget.userId);
    allProductsFuture = apiService.fetchAllProducts();
  }

  @override
  void didUpdateWidget(HomeScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.userId != widget.userId) {
      setState(() {
        recommendedProductsFuture = apiService.fetchRecommendedProducts(widget.userId);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          const SizedBox(height: 30),
          _buildCustomAppBar(context),
          const SizedBox(height: 20),
          _buildSearchBar(),
          _buildCategorySection(),

          FutureBuilder<List<Map<String, dynamic>>>(
            future: allProductsFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return CircularProgressIndicator();
              } else if (snapshot.hasError) {
                return Text('Error: ${snapshot.error}');
              } else {
                return _buildSection('베스트 상품', snapshot.data ?? [], Colors.grey.shade700, context);
              }
            },
          ),
          FutureBuilder<List<Map<String, dynamic>>>(
            future: recommendedProductsFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return CircularProgressIndicator();
              } else if (snapshot.hasError) {
                return Text('Error: ${snapshot.error}');
              } else {
                return _buildSection('추천 상품', snapshot.data ?? [], Colors.grey.shade700, context);
              }
            },
          ),
          _buildSection2('최근 본 상품', recentlyViewedProducts, Colors.grey.shade700, context),
        ],
      ),
    );
  }

  Widget _buildSection(String title, List<Map<String, dynamic>> products, Color color, BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ProductRecommend(
                          products: products,
                        ),
                      ),
                    );
                  },
                  child: const Text('더보기'),
                  style: TextButton.styleFrom(
                    primary: widget.customBlue,
                  ),
                ),
              ],
            ),
          ),
          SizedBox(
            height: 150,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: products.length,
              itemBuilder: (context, index) {
                return _buildProductCard(products[index], context);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductCard(Map<String, dynamic> product, BuildContext context) {
    return GestureDetector(
      onTap: () {
        final productId = product['product_id'];
        final productTitle = product['title'] ?? 'No Title';
        final productPrice = product['price'] ?? 0;
        if (productId != null && productId is int) {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ProductDetailPage(
                productId: productId,
                productTitle: productTitle,
                productPrice: productPrice.toDouble(),
              ),
            ),
          );
        } else {
          print('Invalid product ID: $productId');
        }
      },
      child: Container(
        width: 120,
        margin: const EdgeInsets.symmetric(horizontal: 8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Image.asset(
              _getImageForProductId(product['product_id']),
              fit: BoxFit.cover,
              height: 100,
            ),
            const SizedBox(height: 8),
            Text(
              product['title'] ?? '',
              style: const TextStyle(fontSize: 14),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }

  String _getImageForProductId(int productId) {
    switch (productId) {
      case 8:
        return 'assets/images/veg2.png';
      case 1:
        return 'assets/images/apple.jpg';
      case 10:
        return 'assets/images/tofu.png';
      case 7:
        return 'assets/images/고구마.jpg';
      case 9:
        return 'assets/images/고등어.jpg';
      default:
        return 'assets/images/veg2.png'; // 기본 이미지
    }
  }

  Widget _buildCustomAppBar(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(Icons.location_on, color: Colors.black),
              const SizedBox(width: 8),
              Text(
                widget.dongName ?? '위치 정보 없음',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black),
              ),
            ],
          ),
          GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => MyCartPage()), // You'll need to implement this
              );
            },
            child: Icon(Icons.shopping_cart, color: Colors.black),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: TextField(
        decoration: InputDecoration(
          hintText: '검색',
          prefixIcon: Icon(Icons.search, color: Colors.grey.shade700),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(30.0),
          ),
          contentPadding: const EdgeInsets.symmetric(vertical: 10.0),
        ),
      ),
    );
  }

  Widget _buildCategorySection() {
    final List<Map<String, String>> categories = [
      {'image': 'assets/images/fruit.png', 'label': '과일'},
      {'image': 'assets/images/vegetable.png', 'label': '채소'},
      {'image': 'assets/images/grain.png', 'label': '곡류'},
      {'image': 'assets/images/seafood.png', 'label': '해산물'},
      {'image': 'assets/images/meat.png', 'label': '육류'},
      {'image': 'assets/images/processed.png', 'label': '가공식품'},
      {'image': 'assets/images/dairy.png', 'label': '유제품 및 계란'},
      {'image': 'assets/images/etc.png', 'label': '기타'},
    ];

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 0),
      child: GridView.builder(
        shrinkWrap: true,
        physics: NeverScrollableScrollPhysics(),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 4,
          mainAxisSpacing: 16,
          crossAxisSpacing: 16,
        ),
        itemCount: categories.length,
        itemBuilder: (context, index) {
          return Column(
            children: [
              Image.asset(
                categories[index]['image']!,
                width: 50,
                height: 50,
              ),
              const SizedBox(height: 8),
              Text(
                categories[index]['label']!,
                style: const TextStyle(fontSize: 14),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSection2(String title, List<Map<String, String>> products, Color titleColor, BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 15.0), // 카테고리와 추천 상품 사이의 간격 조정
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: titleColor),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ProductRecommend(
                          products: products,
                        ),
                      ),
                    );
                  },
                  child: const Text('더보기'),
                  style: TextButton.styleFrom(
                    primary: Color(0xFF76A9E6),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(
            height: 150,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: products.length,
              itemBuilder: (context, index) {
                return _buildProductCard2(products[index], context);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductCard2(Map<String, String> product, BuildContext context) {
    return GestureDetector(
      // onTap: () {
      //   Navigator.push(
      //     context,
      //     MaterialPageRoute(
      //       builder: (context) => ProductDetailPage(), // You'll need to implement this
      //     ),
      //   );
      // },
      child: Container(
        width: 120,
        margin: const EdgeInsets.symmetric(horizontal: 8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Image.asset(
              product['image']!,
              fit: BoxFit.cover,
              height: 100,
            ),
            const SizedBox(height: 8),
            Text(
              product['description']!,
              style: const TextStyle(fontSize: 14),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}
