<!DOCTYPE html>
<html lang="vi" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAW PLASTIC - Chuyên Đồ Nhựa Gia Dụng & Tủ Nhựa Cao Cấp</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Font: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        rawRed: {
                            50: '#fef2f2',
                            100: '#fee2e2',
                            500: '#d32f2f', /* Màu đỏ chủ đạo RAW PLASTIC */
                            600: '#b71c1c',
                            700: '#7f0000',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .scrollbar-hidden::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hidden {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        /* Hiệu ứng bóng đổ và chuyển cảnh mượt */
        .hover-card-effect {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .hover-card-effect:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.15);
        }
    </style>
</head>
<body class="flex flex-col min-h-full font-sans antialiased text-slate-800 bg-[#fbfbfb]">

    <!-- TOP BAR ĐĂNG NHẬP & GIỎ HÀNG NHANH -->
    <div class="bg-neutral-100 border-b border-neutral-200 py-2 text-xs text-neutral-600">
        <div class="max-w-7xl mx-auto px-4 flex justify-between items-center">
            <div class="flex items-center gap-4">
                <button onclick="toggleAdminPanel()" class="hover:text-rawRed-500 font-bold text-neutral-800 flex items-center gap-1">
                    <i class="fa-solid fa-user-shield text-rawRed-500"></i> Trang Admin Quản Trị
                </button>
                <span class="hidden sm:inline text-neutral-300">|</span>
                <span class="hover:text-rawRed-500 cursor-pointer"><i class="fa-solid fa-lock mr-1"></i> Đăng nhập / Đăng ký</span>
            </div>
            <div class="flex items-center gap-4">
                <!-- Đèn báo trạng thái kết nối MongoDB -->
                <div id="db-status-indicator" class="flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                    <span id="db-status-text">Đang kết nối...</span>
                </div>
                <span class="hover:text-rawRed-500 cursor-pointer" onclick="resetFilters()"><i class="fa-solid fa-house mr-1"></i> Trang chủ</span>
                <span class="text-neutral-300">|</span>
                <button onclick="toggleCartDrawer()" class="hover:text-rawRed-500 font-bold flex items-center gap-1">
                    <i class="fa-solid fa-bag-shopping"></i> Giỏ hàng (<span id="top-cart-count" class="text-rawRed-500">0</span>)
                </button>
            </div>
        </div>
    </div>

    <!-- MAIN HEADER: LOGO & SEARCH BAR -->
    <header class="bg-white py-5 border-b border-neutral-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
            
            <!-- Logo RAW PLASTIC -->
            <div class="flex items-center gap-3 cursor-pointer select-none" onclick="resetFilters()">
                <div class="relative w-12 h-12 rounded-full border-4 border-dashed border-rawRed-500 flex items-center justify-center bg-gradient-to-tr from-yellow-400 via-rawRed-500 to-indigo-600 shadow-md">
                    <i class="fa-solid fa-box-open text-white text-xl"></i>
                </div>
                <div>
                    <h1 class="text-2xl font-black tracking-tight text-neutral-900 leading-none">RAW <span class="text-rawRed-500">PLASTIC</span></h1>
                    <p class="text-[10px] font-bold tracking-widest text-neutral-500 uppercase mt-0.5">Nhựa gia dụng & Tủ nhựa cao cấp</p>
                </div>
            </div>

            <!-- Thanh tìm kiếm thông minh thời gian thực -->
            <div class="w-full md:w-2/3 relative">
                <div class="flex">
                    <input type="text" id="global-search" oninput="handleSearch(this.value)" class="w-full border-2 border-rawRed-500 rounded-l-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-0" placeholder="Tìm kiếm tủ nhựa, hộp đựng thực phẩm, bàn ghế nhựa chất lượng cao...">
                    <button class="bg-rawRed-500 hover:bg-rawRed-600 text-white px-6 rounded-r-xl font-bold text-sm transition-colors flex items-center gap-1.5">
                        <i class="fa-solid fa-magnifying-glass"></i> <span class="hidden sm:inline">Tìm kiếm</span>
                    </button>
                </div>
                <!-- Kết quả gợi ý tìm kiếm nhanh -->
                <div id="search-suggestions" class="hidden absolute left-0 right-0 top-full mt-1 bg-white border border-neutral-200 rounded-xl shadow-xl z-50 max-h-60 overflow-y-auto"></div>
            </div>

        </div>
    </header>

    <!-- NAVIGATION BAR -->
    <nav class="bg-white border-b border-neutral-200">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex items-center justify-between">
                <!-- Danh sách Menu liên kết với các ID tương tác chủ động -->
                <div class="flex items-center overflow-x-auto scrollbar-hidden py-1">
                    <button id="nav-home" onclick="resetFilters()" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-rawRed-500 border-b-2 border-rawRed-500 whitespace-nowrap">Trang chủ</button>
                    <button id="nav-about" onclick="showStaticPage('about')" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap">Giới thiệu</button>
                    <button id="nav-cabinets" onclick="selectCategory('cabinets')" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap">Tủ nhựa cao cấp</button>
                    <button id="nav-containers" onclick="selectCategory('containers')" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap">Hộp & Khay kháng khuẩn</button>
                    <button id="nav-houseware" onclick="selectCategory('houseware')" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap">Đồ gia dụng tiện ích</button>
                    <button id="nav-news" onclick="showStaticPage('news')" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap">Tin tức</button>
                    <button id="nav-contact" onclick="showStaticPage('contact')" class="px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap">Liên hệ</button>
                </div>
                <!-- Nút tư vấn AI nổi bật -->
                <button id="ai-trigger-btn" class="my-2 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-md hover:shadow-lg transition-all flex items-center gap-1.5 active:scale-95">
                    <i class="fa-solid fa-robot"></i> Trợ lý Tư vấn AI
                </button>
            </div>
        </div>
    </nav>

    <!-- 4 CAM KẾT VÀNG -->
    <section class="bg-white border-b border-neutral-100 py-3.5 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center sm:text-left">
            <div class="flex items-center gap-3.5 p-2 border-r border-neutral-100 last:border-none">
                <span class="text-2xl text-rawRed-500"><i class="fa-solid fa-truck-fast"></i></span>
                <div>
                    <h4 class="text-xs font-bold text-neutral-900 uppercase">Miễn phí vận chuyển</h4>
                    <p class="text-[10px] text-neutral-500">Cho mọi đơn hàng từ 500.000₫ trở lên</p>
                </div>
            </div>
            <div class="flex items-center gap-3.5 p-2 border-r border-neutral-100 last:border-none">
                <span class="text-2xl text-rawRed-500"><i class="fa-solid fa-rotate"></i></span>
                <div>
                    <h4 class="text-xs font-bold text-neutral-900 uppercase">Đổi trả hàng miễn phí</h4>
                    <p class="text-[10px] text-neutral-500">Đổi trả sản phẩm lỗi trong vòng 3 ngày</p>
                </div>
            </div>
            <div class="flex items-center gap-3.5 p-2 border-r border-neutral-100 last:border-none">
                <span class="text-2xl text-rawRed-500"><i class="fa-solid fa-credit-card"></i></span>
                <div>
                    <h4 class="text-xs font-bold text-neutral-900 uppercase">Thanh toán đa dạng</h4>
                    <p class="text-[10px] text-neutral-500">Chấp nhận chuyển khoản, thẻ, COD tiện lợi</p>
                </div>
            </div>
            <div class="flex items-center gap-3.5 p-2 last:border-none">
                <span class="text-2xl text-rawRed-500 animate-pulse"><i class="fa-solid fa-headset"></i></span>
                <div>
                    <h4 class="text-xs font-bold text-neutral-900 uppercase">Tư vấn chuyên sâu 24/7</h4>
                    <p class="text-[10px] text-neutral-500">Hỗ trợ kỹ thuật trực tuyến miễn phí</p>
                </div>
            </div>
        </div>
    </section>

    <!-- BREADCRUMB & SEO ANALYZER BAR -->
    <div class="bg-neutral-100 border-b border-neutral-200 py-2.5 text-xs">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
            <div id="breadcrumb-container" class="flex items-center gap-2 text-neutral-500">
                <span class="hover:text-rawRed-500 cursor-pointer" onclick="resetFilters()">Trang chủ</span>
            </div>
            <div class="flex items-center gap-3 font-semibold text-neutral-600">
                <span id="click-depth-badge" class="bg-neutral-200 text-neutral-700 px-2.5 py-0.5 rounded text-[10px]">Độ sâu nhấp chuột: 0</span>
                <span id="link-juice-badge" class="bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded text-[10px]">Link Juice truyền: 100%</span>
            </div>
        </div>
    </div>

    <!-- KHU VỰC NỘI DUNG CHÍNH (MAIN SCREEN LAYOUT) -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 py-6">
        
        <!-- Khung cảnh báo hoạt động Offline -->
        <div id="fallback-alert" class="hidden mb-6 p-4 rounded-xl border border-sky-100 bg-sky-50 text-sky-800 flex items-start gap-3 shadow-sm">
            <span class="text-xl">💡</span>
            <div>
                <h4 class="font-bold">Đang chạy chế độ Local Demo</h4>
                <p class="text-xs mt-0.5 text-sky-700">Hệ thống đã kích hoạt cơ sở dữ liệu giả lập mượt mà để bạn kiểm tra toàn diện mọi tính năng và cấu trúc phân cấp Silo đồ nhựa.</p>
            </div>
        </div>

        <!-- BỐ CỤC LƯỚI CHÍNH: SIDEBAR TRÁI (1 COL) & NỘI DUNG PHẢI (3 COLS) -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
            
            <!-- SIDEBAR TRÁI (DANH MỤC, BÁN CHẠY, HỖ TRỢ TRỰC TUYẾN) -->
            <aside class="space-y-6">
                
                <!-- 1. DANH MỤC SẢN PHẨM PHÂN CẤP -->
                <div class="bg-white border border-neutral-200 rounded-xl overflow-hidden shadow-sm">
                    <div class="bg-rawRed-500 text-white px-4 py-3 font-bold text-sm uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-list-ul"></i> Danh mục sản phẩm
                    </div>
                    <div class="divide-y divide-neutral-100">
                        <!-- Tủ nhựa cao cấp -->
                        <div class="p-3.5 space-y-2">
                            <button onclick="selectCategory('cabinets')" class="w-full text-left font-bold text-xs text-neutral-800 hover:text-rawRed-500 transition-colors uppercase tracking-wide flex justify-between items-center">
                                <span>📦 Tủ Nhựa Cao Cấp</span>
                                <i class="fa-solid fa-chevron-right text-[10px] text-neutral-400"></i>
                            </button>
                            <div class="pl-3.5 space-y-1.5 pt-1">
                                <button onclick="selectSubcategory('cabinets', 'duytan_cabinets')" class="w-full text-left text-xs text-neutral-500 hover:text-rawRed-500 transition-colors flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full bg-neutral-300"></span> Tủ nhựa Duy Tân siêu bền
                                </button>
                                <button onclick="selectSubcategory('cabinets', 'songlong_cabinets')" class="w-full text-left text-xs text-neutral-500 hover:text-rawRed-500 transition-colors flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full bg-neutral-300"></span> Tủ nhựa Song Long đa sắc
                                </button>
                            </div>
                        </div>

                        <!-- Hộp & Khay kháng khuẩn -->
                        <div class="p-3.5 space-y-2">
                            <button onclick="selectCategory('containers')" class="w-full text-left font-bold text-xs text-neutral-800 hover:text-rawRed-500 transition-colors uppercase tracking-wide flex justify-between items-center">
                                <span>🍱 Hộp & Khay Kháng Khuẩn</span>
                                <i class="fa-solid fa-chevron-right text-[10px] text-neutral-400"></i>
                            </button>
                            <div class="pl-3.5 space-y-1.5 pt-1">
                                <button onclick="selectSubcategory('containers', 'inochi_boxes')" class="w-full text-left text-xs text-neutral-500 hover:text-rawRed-500 transition-colors flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full bg-neutral-300"></span> Hộp thực phẩm Inochi
                                </button>
                                <button onclick="selectSubcategory('containers', 'utility_trays')" class="w-full text-left text-xs text-neutral-500 hover:text-rawRed-500 transition-colors flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full bg-neutral-300"></span> Khay nhựa tiện ích đa năng
                                </button>
                            </div>
                        </div>

                        <!-- Đồ gia dụng tiện ích -->
                        <div class="p-3.5 space-y-2">
                            <button onclick="selectCategory('houseware')" class="w-full text-left font-bold text-xs text-neutral-800 hover:text-rawRed-500 transition-colors uppercase tracking-wide flex justify-between items-center">
                                <span>🪑 Đồ Gia Dụng Tiện Ích</span>
                                <i class="fa-solid fa-chevron-right text-[10px] text-neutral-400"></i>
                            </button>
                            <div class="pl-3.5 space-y-1.5 pt-1">
                                <button onclick="selectSubcategory('houseware', 'chairs_tables')" class="w-full text-left text-xs text-neutral-500 hover:text-rawRed-500 transition-colors flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full bg-neutral-300"></span> Bàn ghế nhựa tiện lợi
                                </button>
                                <button onclick="selectSubcategory('houseware', 'shelves_bins')" class="w-full text-left text-xs text-neutral-500 hover:text-rawRed-500 transition-colors flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full bg-neutral-300"></span> Kệ nhựa & Thùng rác thông minh
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. SẢN PHẨM BÁN CHẠY (BEST SELLERS) -->
                <div class="bg-white border border-neutral-200 rounded-xl overflow-hidden shadow-sm">
                    <div class="bg-rawRed-500 text-white px-4 py-3 font-bold text-sm uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-fire"></i> Sản phẩm bán chạy
                    </div>
                    <div id="best-sellers-list" class="p-3 divide-y divide-neutral-100 space-y-3"></div>
                </div>

                <!-- 3. HỖ TRỢ TRỰC TUYẾN -->
                <div class="bg-white border border-neutral-200 rounded-xl overflow-hidden shadow-sm p-4 space-y-3 text-center">
                    <h3 class="font-bold text-neutral-900 text-sm uppercase tracking-wider border-b border-neutral-100 pb-2 flex items-center justify-center gap-2 text-rawRed-500">
                        <i class="fa-solid fa-headset"></i> Hỗ trợ trực tuyến
                    </h3>
                    <div>
                        <p class="text-xs font-semibold text-neutral-700">Tư vấn chọn mua đồ nhựa</p>
                        <p class="text-[10px] text-neutral-400 mt-1">Chat trực tuyến hỗ trợ tức thì</p>
                    </div>
                    <div class="flex flex-col gap-2 pt-1">
                        <a href="skype:live:rawplastic?chat" class="bg-sky-500 hover:bg-sky-600 text-white py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-1.5 transition-colors">
                            <i class="fa-brands fa-skype"></i> Skype tư vấn ngay
                        </a>
                        <a href="https://zalo.me" target="_blank" class="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-1.5 transition-colors">
                            <i class="fa-solid fa-message"></i> Zalo nhắn tin
                        </a>
                    </div>
                </div>

                <!-- 4. KHUNG GIẢ LẬP LIÊN KẾT FACEBOOK FANPAGE -->
                <div class="bg-white border border-neutral-200 rounded-xl overflow-hidden shadow-sm p-4 text-center">
                    <h3 class="font-bold text-neutral-900 text-xs uppercase tracking-wider border-b border-neutral-100 pb-2 mb-3 text-left flex items-center gap-1.5">
                        <i class="fa-brands fa-facebook text-blue-600 text-sm"></i> Fanpage RAW PLASTIC
                    </h3>
                    <div class="bg-slate-100 rounded-xl p-6 border-2 border-dashed border-neutral-200 text-slate-500 flex flex-col items-center justify-center">
                        <i class="fa-solid fa-users text-2xl text-blue-600 mb-2"></i>
                        <p class="text-xs font-bold text-slate-700">Cộng đồng Đồ Nhựa Tiện Ích</p>
                        <p class="text-[10px] text-slate-400 mt-1">24,530 thành viên yêu thích</p>
                        <button class="mt-3 bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-lg text-[10px] font-bold transition-colors">
                            <i class="fa-solid fa-thumbs-up"></i> Thích Trang
                        </button>
                    </div>
                </div>

            </aside>

            <!-- KHU VỰC HIỂN THỊ NỘI DUNG SẢN PHẨM (BÊN PHẢI) -->
            <section class="lg:col-span-3 space-y-6">
                
                <!-- BẢNG ĐIỀU KHIỂN QUẢN TRỊ ADMIN (ADMIN PANEL) - CHỈ HIỂN THỊ KHI BẬT -->
                <div id="admin-panel-container" class="hidden bg-white border-2 border-indigo-500 rounded-2xl p-6 shadow-xl space-y-6">
                    <div class="flex justify-between items-center border-b border-neutral-200 pb-3">
                        <div class="flex items-center gap-2">
                            <span class="text-2xl">⚙️</span>
                            <div>
                                <h3 class="font-black text-lg text-neutral-950">Bảng Quản Trị Hệ Thống (Admin Panel)</h3>
                                <p class="text-[10px] text-indigo-600 font-bold uppercase">Kết nối và quản lý cơ sở dữ liệu MongoDB trực tiếp</p>
                            </div>
                        </div>
                        <button onclick="toggleAdminPanel()" class="bg-neutral-100 hover:bg-neutral-200 text-neutral-600 font-bold px-3 py-1 rounded-lg text-xs">
                            Đóng Admin
                        </button>
                    </div>

                    <!-- 1. Form thêm sản phẩm mới -->
                    <form id="admin-product-form" class="bg-indigo-50/50 border border-indigo-100 p-5 rounded-xl space-y-4">
                        <h4 class="font-bold text-xs text-indigo-900 uppercase tracking-wider flex items-center gap-1">
                            <i class="fa-solid fa-plus-circle"></i> Thêm sản phẩm mới vào MongoDB
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Tên sản phẩm *</label>
                                <input type="text" id="admin-p-name" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500" placeholder="Ví dụ: Tủ nhựa Duy Tân Mina 5 tầng">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Biểu tượng (Emoji đại diện) *</label>
                                <input type="text" id="admin-p-image" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500" placeholder="Ví dụ: 📦, 🗄️, 🪑, 🍱">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Giá bán lẻ (VND) *</label>
                                <input type="number" id="admin-p-price" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500" placeholder="Ví dụ: 1450000">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Giá gốc/Giá cũ (VND)</label>
                                <input type="number" id="admin-p-original" class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500" placeholder="Ví dụ: 1650000">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Chuyên mục lớn (Cấp 1) *</label>
                                <select id="admin-p-cat" required onchange="updateAdminSubcategories(this.value)" class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500">
                                    <option value="">-- Chọn chuyên mục lớn --</option>
                                    <option value="cabinets">📦 Tủ Nhựa Cao Cấp</option>
                                    <option value="containers">🍱 Hộp & Khay Kháng Khuẩn</option>
                                    <option value="houseware">🪑 Đồ Gia Dụng Tiện Ích</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Chuyên mục con (Cấp 2) *</label>
                                <select id="admin-p-sub" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500">
                                    <option value="">-- Chọn chuyên mục lớn trước --</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Nhãn dán (Badge)</label>
                                <input type="text" id="admin-p-badge" class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500" placeholder="Ví dụ: Bán chạy, Yêu thích, Giảm giá">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Mô tả ngắn *</label>
                                <input type="text" id="admin-p-desc" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:ring-1 focus:ring-indigo-500" placeholder="Thông số kỹ thuật hoặc giới thiệu tiện ích">
                            </div>
                        </div>
                        <button type="submit" class="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs shadow-md transition-all">
                            Lưu và đăng bán lên MongoDB
                        </button>
                    </form>

                    <!-- 2. Phần quản trị dữ liệu / Seed dữ liệu từ Front lên DB -->
                    <div class="border-t border-neutral-200 pt-5 space-y-4">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-indigo-50 p-4 rounded-xl border border-indigo-100">
                            <div>
                                <h4 class="font-bold text-xs text-neutral-900">Tính năng: Nạp/Khôi phục cơ sở dữ liệu (Database Seeding)</h4>
                                <p class="text-[10px] text-neutral-500 mt-0.5">Nhấp để nạp nhanh 24 sản phẩm đồ nhựa gia dụng chuẩn Silo từ bộ nhớ đệm lên MongoDB của bạn.</p>
                            </div>
                            <button onclick="handleDatabaseSeeding()" class="bg-amber-500 hover:bg-amber-600 text-white font-bold px-4 py-2 rounded-xl text-xs shadow transition-all shrink-0">
                                <i class="fa-solid fa-database mr-1"></i> Nhập 24 sản phẩm mẫu lên DB
                            </button>
                        </div>

                        <!-- 3. Bảng danh sách sản phẩm hiện hành với nút xóa -->
                        <div class="space-y-2">
                            <h4 class="font-bold text-xs text-neutral-800 uppercase tracking-wider flex items-center justify-between">
                                <span>Danh sách sản phẩm trong MongoDB</span>
                                <span id="admin-product-count" class="text-[10px] bg-neutral-100 text-neutral-600 px-2 py-0.5 rounded-full">0 sản phẩm</span>
                            </h4>
                            <div class="max-h-60 overflow-y-auto border border-neutral-200 rounded-xl divide-y divide-neutral-100">
                                <div id="admin-products-list-container" class="p-2 space-y-2">
                                    <!-- Danh sách các sản phẩm có nút xóa kết xuất động -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BANNER QUẢNG CÁO LỚN CHÍNH (TỦ NHỰA DUY TÂN) - Thêm ID điều khiển -->
                <div id="main-promo-banner" class="relative bg-gradient-to-r from-neutral-900 to-neutral-800 rounded-2xl overflow-hidden h-72 md:h-96 flex items-center px-8 md:px-16 text-white shadow-md">
                    <!-- Ảnh nền mờ nghệ thuật -->
                    <div class="absolute inset-0 bg-cover bg-center opacity-40 filter blur-sm" style="background-image: url('https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&q=80&w=1000');"></div>
                    
                    <div class="relative z-10 max-w-lg space-y-4">
                        <span class="bg-rawRed-500 text-white text-[10px] font-extrabold px-3 py-1 rounded-full uppercase tracking-widest">Sản phẩm tiêu biểu</span>
                        <h2 class="text-3xl md:text-5xl font-black tracking-tight leading-tight">TỦ NHỰA DUY TÂN <br><span class="text-yellow-400">GIẢM NGAY 10%</span></h2>
                        <p class="text-xs text-neutral-300 leading-relaxed">Dòng tủ nhựa gia đình huyền thoại sở hữu cấu trúc ngăn tủ kéo mượt mà, khung nhựa nguyên sinh vô cùng chắc chắn và an toàn cho sức khỏe của bé và gia đình.</p>
                        <div class="pt-2 flex gap-3">
                            <button onclick="selectCategory('cabinets')" class="bg-rawRed-500 hover:bg-rawRed-600 text-white px-6 py-2.5 rounded-xl text-xs font-bold shadow-lg transition-colors">
                                Khám phá ngay <i class="fa-solid fa-arrow-right ml-1"></i>
                            </button>
                            <button onclick="sendQuickQuestion('Tư vấn cho tôi dòng tủ nhựa Duy Tân cao cấp')" class="bg-white/20 hover:bg-white/30 text-white px-5 py-2.5 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-robot"></i> Hỏi Trợ Lý AI
                            </button>
                        </div>
                    </div>
                </div>

                <!-- TIÊU ĐỀ VIEW HIỆN TẠI - Thêm ID điều khiển -->
                <div id="view-title-block" class="bg-white border border-neutral-200 rounded-xl px-5 py-4 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                    <div>
                        <h2 id="view-title" class="text-lg font-extrabold text-neutral-900 tracking-tight flex items-center gap-2">
                            <i class="fa-solid fa-box-open text-rawRed-500"></i> Tất cả đồ nhựa & tủ nhựa gia dụng
                        </h2>
                        <p id="view-description" class="text-xs text-neutral-500 mt-1">Duyệt và mua sắm các thiết bị tiện ích gia đình hàng đầu được RAW PLASTIC cam kết chất lượng chính hãng</p>
                    </div>
                    <span id="products-count-badge" class="bg-neutral-100 text-neutral-600 px-3.5 py-1.5 rounded-full text-xs font-bold">24 sản phẩm</span>
                </div>

                <!-- LƯỚI KHUNG SẢN PHẨM CHÍNH -->
                <div id="products-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    <!-- Kết xuất dữ liệu sản phẩm tự động qua Javascript -->
                </div>

                <!-- BANNER QUẢNG CÁO PHỤ (INOCHI & ĐỒ DÙNG) - Thêm ID điều khiển -->
                <div id="secondary-banners-block" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-neutral-950 text-white rounded-xl p-6 flex items-center justify-between shadow-sm relative overflow-hidden group">
                        <div class="absolute inset-0 bg-cover bg-center opacity-30 group-hover:scale-105 transition-transform duration-500" style="background-image: url('https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&q=80&w=600');"></div>
                        <div class="relative z-10 max-w-[60%] space-y-2">
                            <span class="text-rawRed-500 font-extrabold text-[10px] uppercase tracking-wider block">Ưu đãi Inochi Nhật Bản</span>
                            <h4 class="text-lg font-extrabold leading-tight">Giảm giá 10% các sản phẩm kháng khuẩn</h4>
                            <p class="text-[10px] text-neutral-300 leading-relaxed">Công nghệ ion bạc kháng khuẩn vượt trội an toàn tuyệt đối.</p>
                            <button onclick="selectCategory('containers')" class="mt-2 text-[10px] font-bold text-yellow-400 flex items-center gap-1 hover:underline">
                                Xem ngay <i class="fa-solid fa-circle-arrow-right"></i>
                            </button>
                        </div>
                        <span class="text-6xl text-white/10 relative z-10"><i class="fa-solid fa-kitchen-set"></i></span>
                    </div>

                    <div class="bg-neutral-950 text-white rounded-xl p-6 flex items-center justify-between shadow-sm relative overflow-hidden group">
                        <div class="absolute inset-0 bg-cover bg-center opacity-30 group-hover:scale-105 transition-transform duration-500" style="background-image: url('https://images.unsplash.com/photo-1581579438747-1dc8d1e0ca96?auto=format&fit=crop&q=80&w=600');"></div>
                        <div class="relative z-10 max-w-[60%] space-y-2">
                            <span class="text-emerald-400 font-extrabold text-[10px] uppercase tracking-wider block">Trải nghiệm đỉnh cao</span>
                            <h4 class="text-lg font-extrabold leading-tight">Dùng thử sản phẩm 15 ngày miễn phí</h4>
                            <p class="text-[10px] text-neutral-300 leading-relaxed">Hoàn trả không mất phí nếu chưa thực sự hài lòng.</p>
                            <button onclick="showStaticPage('about')" class="mt-2 text-[10px] font-bold text-emerald-400 flex items-center gap-1 hover:underline">
                                Xem thể lệ <i class="fa-solid fa-circle-arrow-right"></i>
                            </button>
                        </div>
                        <span class="text-6xl text-white/10 relative z-10"><i class="fa-solid fa-shield-halved"></i></span>
                    </div>
                </div>

                <!-- KHU TRÌNH BÀY NỘI DUNG TĨNH -->
                <div id="static-content-block" class="hidden bg-white border border-neutral-200 rounded-xl p-6 shadow-sm space-y-4"></div>

            </section>

        </div>

    </main>

    <!-- GIỎ HÀNG SIDEBAR DRAWER -->
    <div id="cart-drawer" class="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-white shadow-2xl border-l border-neutral-200 transform translate-x-full transition-transform duration-300 ease-in-out flex flex-col hidden">
        <div class="px-6 py-5 border-b border-neutral-200 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <i class="fa-solid fa-bag-shopping text-rawRed-500 text-xl"></i>
                <h3 class="text-lg font-bold text-neutral-900">Giỏ hàng của bạn</h3>
            </div>
            <button onclick="toggleCartDrawer()" class="text-neutral-400 hover:text-neutral-600 p-2 rounded-lg hover:bg-neutral-50 transition-colors">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
        </div>

        <div id="cart-items-container" class="flex-grow overflow-y-auto p-6 space-y-4"></div>

        <div class="border-t border-neutral-200 p-6 bg-neutral-50 space-y-4">
            <div class="flex justify-between items-center font-bold text-neutral-950 text-lg">
                <span>Tổng tiền tạm tính:</span>
                <span id="cart-total" class="text-rawRed-500">0₫</span>
            </div>
            <button onclick="openCheckoutModal()" class="w-full py-3 bg-rawRed-500 hover:bg-rawRed-600 text-white font-bold rounded-xl shadow-lg shadow-rawRed-500/20 transition-all active:scale-[0.98]">
                Tiến hành đặt hàng ngay
            </button>
        </div>
    </div>

    <!-- MODAL THANH TOÁN -->
    <div id="checkout-modal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm hidden">
        <div class="bg-white rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[90vh]">
            <div class="px-6 py-4 bg-neutral-50 border-b border-neutral-200 flex items-center justify-between">
                <h3 class="font-extrabold text-base text-neutral-950 flex items-center gap-2">
                    <i class="fa-solid fa-file-invoice-dollar text-rawRed-500"></i> Thông Tin & Thanh Toán Đơn Hàng
                </h3>
                <button onclick="closeCheckoutModal()" class="text-neutral-400 hover:text-neutral-600">
                    <i class="fa-solid fa-xmark text-xl"></i>
                </button>
            </div>
            
            <form id="order-form" class="p-6 space-y-4 overflow-y-auto">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Họ và tên người nhận</label>
                        <input type="text" id="customer-name" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-rawRed-500" placeholder="Nguyễn Văn A">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Số điện thoại liên hệ</label>
                        <input type="tel" id="customer-phone" required class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-rawRed-500" placeholder="0987xxxxxx">
                    </div>
                </div>
                <div>
                    <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Địa chỉ nhận hàng</label>
                    <textarea id="customer-address" required rows="2" class="w-full border border-neutral-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-rawRed-500" placeholder="Nhập số nhà, tên đường, phường/xã, quận/huyện..."></textarea>
                </div>
                
                <div>
                    <label class="block text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-1">Phương thức thanh toán</label>
                    <div class="grid grid-cols-2 gap-3 mt-1">
                        <label class="flex items-center gap-2 border border-rawRed-500 bg-rawRed-50/50 p-3 rounded-lg cursor-pointer">
                            <input type="radio" name="payment-method" value="cod" checked onchange="toggleQRDisplay(false)" class="text-rawRed-500 focus:ring-rawRed-500">
                            <div>
                                <span class="text-xs font-bold block">COD</span>
                                <span class="text-[9px] text-neutral-500 block">Thanh toán tiền mặt khi nhận hàng</span>
                            </div>
                        </label>
                        <label class="flex items-center gap-2 border border-neutral-200 p-3 rounded-lg cursor-pointer hover:bg-slate-50">
                            <input type="radio" name="payment-method" value="banking" onchange="toggleQRDisplay(true)" class="text-rawRed-500 focus:ring-rawRed-500">
                            <div>
                                <span class="text-xs font-bold block">Chuyển khoản</span>
                                <span class="text-[9px] text-neutral-500 block">Quét mã VietQR chuyển khoản</span>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Khu vực hiển thị chuyển khoản ngân hàng giả lập VietQR -->
                <div id="qr-payment-area" class="hidden bg-neutral-50 border border-neutral-200 p-4 rounded-xl flex flex-col items-center justify-center space-y-3">
                    <p class="text-xs font-bold text-neutral-700 text-center">Quét mã QR sau để thực hiện chuyển khoản an toàn</p>
                    <div class="bg-white p-3 rounded-xl border border-neutral-200 shadow-sm relative">
                        <div class="w-48 h-48 bg-slate-100 flex flex-col items-center justify-center text-center p-3 border-2 border-dashed border-neutral-300">
                            <i class="fa-solid fa-qrcode text-6xl text-slate-700 mb-1 animate-pulse"></i>
                            <span class="text-[10px] font-black text-blue-600 block">VIETQR - NAPAS247</span>
                            <span class="text-[9px] text-neutral-500 block">Ngân hàng MB Bank</span>
                            <span class="text-[9px] text-neutral-700 font-bold block">Chủ TK: RAW PLASTIC SHOP</span>
                            <span class="text-[9px] text-rawRed-500 font-extrabold block">Số tiền: <span id="qr-total-amount">0₫</span></span>
                        </div>
                    </div>
                    <p class="text-[10px] text-neutral-400">Hệ thống sẽ tự động xác minh giao dịch của bạn sau khi tiền được gửi đi thành công.</p>
                </div>

                <div class="border-t border-neutral-200 pt-4 mt-6">
                    <button type="submit" class="w-full py-3 bg-gradient-to-r from-rawRed-500 to-rawRed-700 hover:from-rawRed-600 hover:to-rawRed-800 text-white font-bold rounded-xl shadow-lg transition-all active:scale-95">
                        Xác nhận đặt hàng và hoàn tất (<span id="modal-total-amount">0₫</span>)
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- PANEL TRỢ LÝ TƯ VẤN AI (CHATBOT SIDEBAR) -->
    <div id="ai-chat-drawer" class="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-white shadow-2xl border-l border-slate-200 transform translate-x-full transition-transform duration-300 ease-in-out flex flex-col hidden">
        <div class="px-6 py-4 bg-gradient-to-r from-neutral-950 to-neutral-800 text-white flex items-center justify-between">
            <div class="flex items-center gap-2">
                <i class="fa-solid fa-robot text-lg text-rawRed-500 animate-pulse"></i>
                <div>
                    <h3 class="font-extrabold text-sm tracking-tight text-white">Trợ lý Mua sắm AI - RAW PLASTIC</h3>
                    <p class="text-[10px] text-slate-300">Nhân viên tư vấn kỹ thuật sản phẩm gia dụng 24/7</p>
                </div>
            </div>
            <button id="ai-chat-close-btn" class="text-neutral-400 hover:text-white p-1">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
        </div>

        <div id="ai-messages-container" class="flex-grow overflow-y-auto p-4 space-y-4">
            <div class="flex gap-2.5 items-start">
                <span class="text-xl bg-rawRed-50 p-2 rounded-xl shrink-0 select-none">🤖</span>
                <div class="bg-neutral-50 text-slate-800 text-xs px-3.5 py-2.5 rounded-2xl max-w-[85%] leading-relaxed border border-neutral-100 shadow-sm space-y-1.5">
                    <p>Xin kính chào quý khách! Tôi là trợ lý chuyên gia tư vấn từ <strong>RAW PLASTIC</strong>.</p>
                    <p>Tôi am hiểu toàn bộ các thiết bị tủ nhựa, hộp đựng, bàn ghế tại cửa hàng, sẵn sàng tư vấn:</p>
                    <ul class="list-disc pl-4 space-y-1">
                        <li>Lựa chọn tủ nhựa đựng quần áo cho bé (Duy Tân, Song Long).</li>
                        <li>Đề xuất bộ hộp đựng thực phẩm Inochi kháng khuẩn an toàn.</li>
                        <li>Giải thích sự khác biệt chất liệu nhựa PP, nhựa ABS nguyên sinh.</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="p-3 bg-neutral-50 border-t border-neutral-100 flex gap-2 overflow-x-auto scrollbar-hidden">
            <button onclick="sendQuickQuestion('Tư vấn cho tôi tủ nhựa Duy Tân 5 tầng')" class="shrink-0 text-[10px] bg-white border border-neutral-200 px-3 py-1.5 rounded-full hover:border-rawRed-500 hover:text-rawRed-500 font-bold transition-colors">
                📦 Tủ Duy Tân 5 tầng?
            </button>
            <button onclick="sendQuickQuestion('Nên mua hộp thực phẩm Inochi loại nào tốt?')" class="shrink-0 text-[10px] bg-white border border-neutral-200 px-3 py-1.5 rounded-full hover:border-rawRed-500 hover:text-rawRed-500 font-bold transition-colors">
                🍱 Hộp nhựa Inochi?
            </button>
            <button onclick="sendQuickQuestion('Các sản phẩm nhựa gia dụng Song Long tốt nhất?')" class="shrink-0 text-[10px] bg-white border border-neutral-200 px-3 py-1.5 rounded-full hover:border-rawRed-500 hover:text-rawRed-500 font-bold transition-colors">
                🪑 Nhựa Song Long?
            </button>
        </div>

        <form id="ai-chat-form" class="p-3 border-t border-neutral-200 bg-white flex gap-2">
            <input type="text" id="ai-input" required class="flex-grow border border-neutral-200 rounded-xl px-4 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-rawRed-500" placeholder="Đặt câu hỏi về kích thước, dung tích, tư vấn mua sắm...">
            <button type="submit" class="bg-rawRed-500 hover:bg-rawRed-600 text-white rounded-xl px-4 py-2 text-xs font-bold transition-all shrink-0">
                Gửi đi
            </button>
        </form>
    </div>

    <!-- FOOTER CHÂN TRANG ĐÚNG MẪU SAPO VIỆT NAM -->
    <footer class="bg-neutral-900 text-white border-t border-neutral-800 py-8 mt-12">
        <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-3">
                <div class="flex items-center gap-2">
                    <div class="w-10 h-10 rounded-full border-2 border-dashed border-rawRed-500 flex items-center justify-center bg-rawRed-500 shadow">
                        <i class="fa-solid fa-box-open text-white text-base"></i>
                    </div>
                    <h2 class="text-xl font-black tracking-tight text-white leading-none">RAW <span class="text-rawRed-500">PLASTIC</span></h2>
                </div>
                <p class="text-xs text-neutral-400 leading-relaxed">Cửa hàng uy tín hàng đầu chuyên cung cấp tủ nhựa Duy Tân, Song Long cao cấp cùng các sản phẩm hộp khay nhựa gia dụng, kháng khuẩn thông minh Nhật Bản.</p>
            </div>
            <div>
                <h3 class="font-bold text-sm uppercase tracking-wider text-white border-l-4 border-rawRed-500 pl-3 mb-4">Danh mục hữu ích</h3>
                <ul class="space-y-2 text-xs text-neutral-400">
                    <li><button onclick="resetFilters()" class="hover:text-rawRed-500 transition-colors">Trang chủ cửa hàng</button></li>
                    <li><button onclick="showStaticPage('about')" class="hover:text-rawRed-500 transition-colors">Về RAW PLASTIC</button></li>
                    <li><button onclick="showStaticPage('news')" class="hover:text-rawRed-500 transition-colors">Tin tức công nghệ đồ nhựa</button></li>
                    <li><button onclick="showStaticPage('contact')" class="hover:text-rawRed-500 transition-colors">Trung tâm bảo hành & Liên hệ</button></li>
                </ul>
            </div>
            <div>
                <h3 class="font-bold text-sm uppercase tracking-wider text-white border-l-4 border-rawRed-500 pl-3 mb-4">Thông tin liên hệ</h3>
                <ul class="space-y-2 text-xs text-neutral-400">
                    <li><i class="fa-solid fa-location-dot mr-2 text-rawRed-500"></i> Địa chỉ: Toà nhà Ladeco, 266 Đội Cấn, Ba Đình, Hà Nội</li>
                    <li><i class="fa-solid fa-envelope mr-2 text-rawRed-500"></i> Email: support@sapo.vn</li>
                </ul>
            </div>
        </div>
    </footer>

    <!-- SAPO BOTTOM BANNER -->
    <div class="bg-[#00c569] text-white py-3.5">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-3">
            <div class="flex items-center gap-4 text-xs font-bold">
                <span class="flex items-center gap-1"><i class="fa-solid fa-globe text-base"></i> www.sapo.vn</span>
                <span class="flex items-center gap-1"><i class="fa-solid fa-headset text-base"></i> Hỗ trợ trực tuyến 24/7</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="text-[10px] font-bold text-white/90">Thiết kế website bán hàng cao cấp bởi</span>
                <span class="bg-[#0052cc] text-white px-3 py-1 rounded-lg font-black text-xs tracking-wider shadow shadow-blue-800">Sapo</span>
            </div>
        </div>
    </div>

    <!-- HỘP THOẠI TOAST THÔNG BÁO TÙY BIẾN -->
    <div id="toast" class="fixed bottom-5 left-1/2 -translate-x-1/2 z-50 transform translate-y-10 opacity-0 transition-all duration-300 pointer-events-none">
        <div class="bg-neutral-900 text-white px-5 py-3 rounded-xl shadow-xl flex items-center gap-2 text-sm font-semibold border border-neutral-800">
            <span id="toast-icon">✨</span>
            <span id="toast-message">Đã thực hiện!</span>
        </div>
    </div>

    <script>
        // Địa chỉ máy chủ Backend phục vụ tích hợp
        const API_BASE = "http://localhost:5000/api";
        
        let allProducts = [];
        let filteredProducts = [];
        let cart = [];
        let isBackendConnected = false;
        let isAdminVisible = false;

        // Trạng thái lọc cấu trúc Silo hiện hữu
        let currentSiloState = {
            level: 0, 
            category: 'all',
            subcategory: 'all'
        };

        // Danh mục con map Cấp 2 tương ứng Cấp 1
        const SUBCATEGORIES_MAP = {
            cabinets: [
                { id: 'duytan_cabinets', name: 'Tủ nhựa Duy Tân siêu bền' },
                { id: 'songlong_cabinets', name: 'Tủ nhựa Song Long đa sắc' }
            ],
            containers: [
                { id: 'inochi_boxes', name: 'Hộp thực phẩm Inochi' },
                { id: 'utility_trays', name: 'Khay nhựa tiện ích đa năng' }
            ],
            houseware: [
                { id: 'chairs_tables', name: 'Bàn ghế nhựa tiện lợi' },
                { id: 'shelves_bins', name: 'Kệ nhựa & Thùng rác thông minh' }
            ]
        };

        // Danh sách toàn vẹn 24 sản phẩm tương ứng mô hình Silo đồ nhựa 3 cấp
        const localBackupProducts = [
            // ==================== 1. TỦ NHỰA CAO CẤP (cabinets) ====================
            // Phân cấp con 1.1: Tủ nhựa Duy Tân (duytan_cabinets)
            { id: 1, name: "Tủ nhựa Duy Tân Mina 5 tầng 6 ngăn kéo", price: 1450000, originalPrice: 1650000, category: "cabinets", subcategory: "duytan_cabinets", image: "📦", rating: 4.9, reviews: 340, badge: "Bán chạy", description: "Họa tiết trang nhã, thiết kế 5 tầng tiện lợi rộng rãi đựng quần áo cho bé." },
            { id: 2, name: "Tủ nhựa Duy Tân Tabi-S 5 tầng cao cấp", price: 1550000, originalPrice: 1800000, category: "cabinets", subcategory: "duytan_cabinets", image: "🗄️", rating: 4.8, reviews: 220, badge: "Yêu thích", description: "Vật liệu nhựa PP/ABS chính phẩm siêu bền, không mối mọt cong vênh." },
            { id: 3, name: "Tủ treo quần áo Duy Tân Wing 4 cánh lớn", price: 2890000, originalPrice: 3200000, category: "cabinets", subcategory: "duytan_cabinets", image: "🚪", rating: 4.7, reviews: 185, badge: "Giảm giá", description: "Thiết kế treo đồ tiện lợi, có ngăn kéo và khóa tủ riêng biệt an toàn." },
            { id: 4, name: "Tủ nhựa Duy Tân Tomi mini 4 ngăn nhỏ gọn", price: 290000, originalPrice: 350000, category: "cabinets", subcategory: "duytan_cabinets", image: "📥", rating: 4.6, reviews: 110, badge: "Mới nhất", description: "Thích hợp đặt trên bàn học, đựng đồ trang điểm hoặc vật dụng cá nhân nhỏ." },

            // Phân cấp con 1.2: Tủ nhựa Song Long (songlong_cabinets)
            { id: 5, name: "Tủ nhựa Song Long Pucca 5 tầng 6 ngăn", price: 1390000, originalPrice: 1550000, category: "cabinets", subcategory: "songlong_cabinets", image: "📦", rating: 4.9, reviews: 410, badge: "Bán chạy", description: "Cấu trúc ngăn kéo thông minh trơn tru, chất nhựa dẻo chịu lực va đập cực tốt." },
            { id: 6, name: "Tủ nhựa Song Long Panda hoạt họa 4 tầng", price: 1150000, originalPrice: 1300000, category: "cabinets", subcategory: "songlong_cabinets", image: "🗄️", rating: 4.8, reviews: 295, badge: "Cổ điển", description: "In hình gấu Panda dễ thương sắc nét, kích thước phù hợp mọi phòng ngủ của bé." },
            { id: 7, name: "Tủ nhựa Song Long Milan 6 ngăn sang trọng", price: 2390000, originalPrice: 2660000, category: "cabinets", subcategory: "songlong_cabinets", image: "🚪", rating: 4.8, reviews: 155, badge: "Mới nhất", description: "Họa tiết giả vân gỗ cao cấp sang trọng, dễ dàng lắp ráp và vệ sinh lau chùi." },
            { id: 8, name: "Tủ nhựa Song Long T222 mini xếp gọn", price: 635000, originalPrice: 830000, category: "cabinets", subcategory: "songlong_cabinets", image: "📥", rating: 4.7, reviews: 125, badge: "", description: "Phù hợp để cạnh giường ngủ tiện dụng, chứa tài liệu, thuốc hoặc phụ kiện gia đình." },

            // ==================== 2. HỘP & KHAY KHÁNG KHUẨN (containers) ====================
            // Phân cấp con 2.1: Hộp thực phẩm Inochi (inochi_boxes)
            { id: 9, name: "Bộ 3 hộp nhựa thực phẩm Inochi Hokkaido", price: 129000, originalPrice: 169000, category: "containers", subcategory: "inochi_boxes", image: "🍱", rating: 4.9, reviews: 190, badge: "Đẳng cấp", description: "Vật liệu nhựa nguyên sinh tích hợp ion bạc kháng khuẩn vượt trội, an toàn trong tủ lạnh." },
            { id: 10, name: "Hộp đựng cơm trưa chia ngăn Inochi cao cấp", price: 85000, originalPrice: 120000, category: "containers", subcategory: "inochi_boxes", image: "🥗", rating: 4.9, reviews: 145, badge: "Bán chạy", description: "Có gioăng silicon kín khít chống tràn nước canh, dùng được trong lò vi sóng." },
            { id: 11, name: "Hộp đựng thực phẩm Hokkaido Inochi 2L", price: 45000, originalPrice: 65000, category: "containers", subcategory: "inochi_boxes", image: "📦", rating: 4.8, reviews: 210, badge: "Giá tốt", description: "Thiết kế xếp chồng thông minh tiết kiệm diện tích, chịu nhiệt độ từ -30 đến 140 độ C." },
            { id: 12, name: "Hũ nhựa gia vị thông minh Inochi kèm thìa", price: 35000, originalPrice: 50000, category: "containers", subcategory: "inochi_boxes", image: "🏺", rating: 4.7, reviews: 310, badge: "Yêu thích", description: "Nắp mở nhanh chóng, đi kèm thìa nhựa tiện dụng, bảo quản gia vị khô ráo tuyệt đối." },

            // Phân cấp con 2.2: Khay nhựa tiện ích (utility_trays)
            { id: 13, name: "Khay nhựa đa năng chia nhiều ngăn kéo", price: 115000, originalPrice: 150000, category: "containers", subcategory: "utility_trays", image: "📥", rating: 4.9, reviews: 180, badge: "Bán chạy", description: "Dành cho bàn làm việc, đựng son mỹ phẩm, văn phòng phẩm vô cùng gọn gàng." },
            { id: 14, name: "Khay nhựa Song Long PB5 công nghiệp", price: 79000, originalPrice: 95000, category: "containers", subcategory: "utility_trays", image: "🧺", rating: 4.8, reviews: 120, badge: "Siêu bền", description: "Nhựa cứng chịu tải lực lớn, ứng dụng nuôi cá, lọc nước hồ cá hoặc đựng dụng cụ." },
            { id: 15, name: "Khay nhựa chia 4 ngăn Song Long PB51", price: 85000, originalPrice: 105000, category: "containers", subcategory: "utility_trays", image: "📥", rating: 4.6, reviews: 245, badge: "Đáng mua", description: "Chia ngăn linh hoạt giúp sắp xếp linh kiện ốc vít cơ khí gọn gàng khoa học." },
            { id: 16, name: "Khay mứt Tết xoay cánh hoa Inochi sang trọng", price: 219000, originalPrice: 280000, category: "containers", subcategory: "utility_trays", image: "🌸", rating: 4.7, reviews: 160, badge: "Tết", description: "Chất liệu nhựa PP cao cấp không chứa BPA độc hại, xoay cánh hoa mở đóng mượt mà." },

            // ==================== 3. ĐỒ GIA DỤNG TIỆN ÍCH (houseware) ====================
            // Phân cấp con 3.1: Bàn ghế nhựa (chairs_tables)
            { id: 17, name: "Ghế nhựa xếp gọn thông minh Duy Tân", price: 145000, originalPrice: 185000, category: "houseware", subcategory: "chairs_tables", image: "🪑", rating: 4.8, reviews: 110, badge: "Khuyên dùng", description: "Dễ dàng gấp phẳng cất đi gọn gàng, chất liệu nhựa dầy chịu lực tới 100kg." },
            { id: 18, name: "Bàn nhựa mầm non Song Long cao cấp", price: 252000, originalPrice: 320000, category: "houseware", subcategory: "chairs_tables", image: "🧱", rating: 4.8, reviews: 85, badge: "Gọn nhẹ", description: "Mặt bàn nhám chống trơn trượt, bốn chân vững chãi chịu tải lớn cho trẻ em ngồi chơi." },
            { id: 19, name: "Ghế nhựa đẩu cao Song Long siêu bền", price: 45000, originalPrice: 60000, category: "houseware", subcategory: "chairs_tables", image: "🪑", rating: 4.6, reviews: 135, badge: "Giá rẻ", description: "Màu sắc nổi bật, chân ghế lót đệm chống trượt bám chặt sàn nhà." },
            { id: 20, name: "Bát ăn dặm bọc nhựa chống nóng Thái Lan", price: 117000, originalPrice: 145000, category: "houseware", subcategory: "chairs_tables", image: "🥣", rating: 4.5, reviews: 92, badge: "", description: "Phía trong lót inox 304 giữ nhiệt cực tốt, bên ngoài bọc nhựa PP cách nhiệt an toàn." },

            // Phân cấp con 3.2: Kệ & Thùng rác (shelves_bins)
            { id: 21, name: "Kệ nhựa gia vị 3 tầng có bánh xe Inochi", price: 345000, originalPrice: 420000, category: "houseware", subcategory: "shelves_bins", image: "🗄️", rating: 4.9, reviews: 175, badge: "Đẳng cấp", description: "Khung chắc chắn, dễ dàng di chuyển luồn vào các khe tủ nhà bếp hẹp tiện ích." },
            { id: 22, name: "Thùng rác nhựa Song Long nắp lật lớn 60L", price: 175000, originalPrice: 220000, category: "houseware", subcategory: "shelves_bins", image: "🗑️", rating: 4.7, reviews: 140, badge: "Khuyên dùng", description: "Dung tích cực lớn, nắp lật tiện lợi, chất nhựa dày dặn chịu nắng mưa ngoài trời bền bỉ." },
            { id: 23, name: "Thùng rác kháng khuẩn đạp chân Inochi 15L", price: 235000, originalPrice: 290000, category: "houseware", subcategory: "shelves_bins", image: "🗑️", rating: 4.8, reviews: 64, badge: "Chuyên nghiệp", description: "Cơ chế đạp chân êm ái, nắp đóng kín khít ngăn mùi hôi và vi khuẩn phát tán hiệu quả." },
            { id: 24, name: "Kệ nhựa chén đĩa Song Long 3 tầng tiện lợi", price: 235000, originalPrice: 290000, category: "houseware", subcategory: "shelves_bins", image: "🍽️", rating: 4.6, reviews: 78, badge: "", description: "Có khay hứng nước chảy xuống sạch sẽ khô ráo, đi kèm ống cắm đũa muỗng tiện lợi." }
        ];

        // Khởi động trang ứng dụng
        window.onload = async function() {
            await checkConnection();
            await loadProducts();
            initCart();
            renderBestSellers();
            setupAdminEventListeners();
        }

        // Kiểm tra kết nối MongoDB qua API Backend
        async function checkConnection() {
            const indicator = document.getElementById('db-status-indicator');
            const textSpan = document.getElementById('db-status-text');
            const fallbackAlert = document.getElementById('fallback-alert');

            try {
                const res = await fetch(`${API_BASE}/status`);
                const data = await res.json();
                
                if (data.status === "connected") {
                    isBackendConnected = true;
                    indicator.className = "flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200";
                    indicator.querySelector('span').className = "w-2 h-2 rounded-full bg-emerald-500";
                    textSpan.textContent = "MongoDB: Đã kết nối";
                    fallbackAlert.classList.add('hidden');
                } else {
                    throw new Error("DB Disconnected");
                }
            } catch (err) {
                isBackendConnected = false;
                indicator.className = "flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200";
                indicator.querySelector('span').className = "w-2 h-2 rounded-full bg-rose-500 animate-pulse";
                textSpan.textContent = "MongoDB: Lỗi kết nối";
                fallbackAlert.classList.remove('hidden');
            }
        }

        // Nạp sản phẩm từ Backend hoặc bộ nhớ offline
        async function loadProducts() {
            try {
                if (!isBackendConnected) throw new Error("Offline Mode");
                const res = await fetch(`${API_BASE}/products`);
                allProducts = await res.json();
            } catch (err) {
                console.warn("Đang chạy ở chế độ offline giả lập.");
                allProducts = localBackupProducts;
            }
            filteredProducts = [...allProducts];
            renderProductsGrid();
            renderAdminProductsTable(); // Cập nhật bảng quản trị cho admin
        }

        // Render lưới sản phẩm nhựa gia dụng chuyên nghiệp
        function renderProductsGrid() {
            const grid = document.getElementById('products-grid');
            const staticBlock = document.getElementById('static-content-block');
            
            // Đảm bảo ẩn khối tĩnh khi duyệt sản phẩm
            staticBlock.classList.add('hidden');
            grid.classList.remove('hidden');

            document.getElementById('products-count-badge').textContent = `${filteredProducts.length} sản phẩm`;

            if (filteredProducts.length === 0) {
                grid.innerHTML = `<div class="col-span-full py-16 text-center text-slate-400 font-bold">Không tìm thấy sản phẩm nhựa nào phù hợp.</div>`;
                return;
            }

            grid.innerHTML = filteredProducts.map(p => {
                const discountPercent = p.originalPrice ? Math.round(((p.originalPrice - p.price) / p.originalPrice) * 100) : 0;
                return `
                    <div class="bg-white border border-neutral-200 rounded-xl overflow-hidden hover-card-effect flex flex-col justify-between group h-full">
                        <div class="relative bg-neutral-50 p-6 flex justify-center items-center h-48 text-6xl select-none">
                            ${p.image}
                            ${discountPercent > 0 ? `<span class="absolute top-3 left-3 bg-rawRed-500 text-white text-[10px] font-black px-2 py-1 rounded-md">-${discountPercent}%</span>` : ''}
                            ${p.badge ? `<span class="absolute top-3 right-3 bg-yellow-400 text-neutral-900 text-[9px] font-extrabold px-2 py-1 rounded-md uppercase tracking-wider">${p.badge}</span>` : ''}
                        </div>
                        <div class="p-4 flex-grow flex flex-col justify-between space-y-3">
                            <div>
                                <span class="text-[9px] font-bold text-neutral-400 uppercase tracking-widest block">${getCategoryNameVi(p.category)} &gt; ${getSubcategoryNameVi(p.subcategory)}</span>
                                <h3 class="font-extrabold text-neutral-800 text-xs mt-1.5 line-clamp-2 hover:text-rawRed-500 cursor-pointer" onclick="sendQuickQuestion('Tư vấn chi tiết về ${p.name}')" title="${p.name}">${p.name}</h3>
                                <div class="flex items-center gap-1.5 mt-2 text-[11px]">
                                    <span class="text-amber-400"><i class="fa-solid fa-star"></i></span>
                                    <span class="font-bold text-neutral-700">${p.rating || 5}</span>
                                    <span class="text-neutral-400">(${p.reviews || 0} đánh giá)</span>
                                </div>
                                <p class="text-[11px] text-neutral-500 mt-2 line-clamp-2 leading-relaxed">${p.description || "Chưa có mô tả ngắn"}</p>
                            </div>
                            <div class="pt-3 border-t border-neutral-100">
                                <div class="flex items-baseline gap-2">
                                    <span class="text-sm font-black text-rawRed-500">${formatVND(p.price)}</span>
                                    ${p.originalPrice ? `<span class="text-xs text-neutral-400 line-through">${formatVND(p.originalPrice)}</span>` : ''}
                                </div>
                                <div class="grid grid-cols-2 gap-2 mt-3">
                                    <button onclick="addToCart(${p.id})" class="py-2 bg-rawRed-500 hover:bg-rawRed-600 text-white font-bold rounded-lg text-[10px] transition-colors flex items-center justify-center gap-1">
                                        <i class="fa-solid fa-cart-plus"></i> Cho vào giỏ
                                    </button>
                                    <button onclick="askAIAbooutProduct('${p.name}')" class="py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg text-[10px] transition-colors flex items-center justify-center gap-1">
                                        <i class="fa-solid fa-robot text-violet-600"></i> Hỏi AI
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        // --- HÀM THIẾT LẬP HOẠT ĐỘNG ACTIVE CHO THANH MENU ĐIỀU HƯỚNG ---
        function setActiveNav(navId) {
            const navIds = ['nav-home', 'nav-about', 'nav-cabinets', 'nav-containers', 'nav-houseware', 'nav-news', 'nav-contact'];
            navIds.forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;
                if (id === navId) {
                    el.className = "px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-rawRed-500 border-b-2 border-rawRed-500 whitespace-nowrap";
                } else {
                    el.className = "px-4 py-3.5 text-xs font-bold uppercase tracking-wider text-neutral-600 hover:text-rawRed-500 border-b-2 border-transparent transition-colors whitespace-nowrap";
                }
            });
        }

        // --- CÁC TÍNH NĂNG ADMIN & KẾT NỐI MONGODB ---

        // Bật tắt bảng Admin Panel
        window.toggleAdminPanel = function() {
            const container = document.getElementById('admin-panel-container');
            if (isAdminVisible) {
                container.classList.add('hidden');
                isAdminVisible = false;
            } else {
                container.classList.remove('hidden');
                isAdminVisible = true;
                container.scrollIntoView({ behavior: 'smooth' });
                renderAdminProductsTable();
            }
        }

        // Cập nhật Subcategories tương ứng khi admin chọn danh mục lớn Cấp 1
        window.updateAdminSubcategories = function(category) {
            const subSelect = document.getElementById('admin-p-sub');
            if (!category) {
                subSelect.innerHTML = `<option value="">-- Chọn chuyên mục lớn trước --</option>`;
                return;
            }

            const subs = SUBCATEGORIES_MAP[category] || [];
            subSelect.innerHTML = subs.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        }

        // Setup các Event Listeners của Admin Form
        function setupAdminEventListeners() {
            const form = document.getElementById('admin-product-form');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                if (!isBackendConnected) {
                    showToast("Lỗi: Cần chạy và kết nối server Backend MongoDB trước để thêm!", "❌");
                    return;
                }

                const name = document.getElementById('admin-p-name').value;
                const image = document.getElementById('admin-p-image').value;
                const price = document.getElementById('admin-p-price').value;
                const originalPrice = document.getElementById('admin-p-original').value;
                const category = document.getElementById('admin-p-cat').value;
                const subcategory = document.getElementById('admin-p-sub').value;
                const badge = document.getElementById('admin-p-badge').value;
                const description = document.getElementById('admin-p-desc').value;

                const payload = { name, image, price, originalPrice, category, subcategory, badge, description };

                try {
                    const res = await fetch(`${API_BASE}/products`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    const data = await res.json();
                    
                    if (data.success) {
                        showToast("Thêm sản phẩm thành công vào MongoDB!", "🎉");
                        form.reset();
                        // Nạp lại dữ liệu mới từ Database
                        await loadProducts();
                    } else {
                        throw new Error(data.message);
                    }
                } catch (err) {
                    showToast("Lỗi khi thêm: " + err.message, "❌");
                }
            });
        }

        // Hiển thị danh sách sản phẩm quản trị trong Admin Panel kèm nút Xóa
        function renderAdminProductsTable() {
            const listContainer = document.getElementById('admin-products-list-container');
            const countBadge = document.getElementById('admin-product-count');
            
            countBadge.textContent = `${allProducts.length} sản phẩm`;

            if (allProducts.length === 0) {
                listContainer.innerHTML = `<div class="text-center text-xs text-neutral-400 py-4">Chưa có sản phẩm nào trong MongoDB.</div>`;
                return;
            }

            listContainer.innerHTML = allProducts.map(p => `
                <div class="flex items-center justify-between bg-neutral-50 p-2.5 rounded-lg border border-neutral-100 text-xs">
                    <div class="flex items-center gap-3 min-w-0">
                        <span class="text-xl bg-white p-1 rounded border select-none shrink-0">${p.image}</span>
                        <div class="min-w-0">
                            <h5 class="font-bold text-neutral-800 truncate" title="${p.name}">${p.name}</h5>
                            <p class="text-[10px] text-neutral-400 font-semibold mt-0.5">${getCategoryNameVi(p.category)} &gt; ${getSubcategoryNameVi(p.subcategory)} | Price: ${formatVND(p.price)}</p>
                        </div>
                    </div>
                    <button onclick="deleteProduct(${p.id})" class="bg-red-50 hover:bg-red-100 text-red-600 font-bold px-2.5 py-1.5 rounded-lg transition-colors border border-red-200 flex items-center gap-1 shrink-0">
                        <i class="fa-solid fa-trash-can"></i> Xóa
                    </button>
                </div>
            `).join('');
        }

        // Xóa sản phẩm qua API Backend
        window.deleteProduct = async function(id) {
            if (!isBackendConnected) {
                showToast("Lỗi: Cần kết nối Backend MongoDB để thực hiện xóa!", "❌");
                return;
            }

            if (!confirm(`Bạn có chắc chắn muốn xóa sản phẩm ID [${id}] khỏi MongoDB?`)) {
                return;
            }

            try {
                const res = await fetch(`${API_BASE}/products/${id}`, { method: "DELETE" });
                const data = await res.json();
                
                if (data.success) {
                    showToast("Đã xóa sản phẩm thành công khỏi MongoDB!", "🗑️");
                    await loadProducts();
                } else {
                    throw new Error(data.message);
                }
            } catch (err) {
                showToast("Lỗi: " + err.message, "❌");
            }
        }

        // Nạp nhanh sỉ dữ liệu 24 sản phẩm mẫu lên MongoDB
        window.handleDatabaseSeeding = async function() {
            if (!isBackendConnected) {
                showToast("Chế độ Offline: Không thể seeding lên MongoDB!", "❌");
                return;
            }

            try {
                const res = await fetch(`${API_BASE}/products/seed-bulk`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(localBackupProducts)
                });
                const data = await res.json();
                
                if (data.success) {
                    showToast("Nạp 24 sản phẩm mẫu lên MongoDB thành công!", "🎉");
                    await loadProducts();
                } else {
                    throw new Error(data.message);
                }
            } catch (err) {
                showToast("Lỗi nạp database: " + err.message, "❌");
            }
        }

        // --- CÁC TÍNH NĂNG DUYỆT SẢN PHẨM KHÁC ---

        // Lọc theo Chuyên mục Cấp 1
        window.selectCategory = function(cat) {
            currentSiloState = { level: 1, category: cat, subcategory: 'all' };
            filteredProducts = allProducts.filter(p => p.category === cat);
            
            // Ẩn các banner quảng cáo gây loãng thông tin chuyên mục
            document.getElementById('main-promo-banner').classList.add('hidden');
            document.getElementById('view-title-block').classList.remove('hidden');
            document.getElementById('products-grid').classList.remove('hidden');
            document.getElementById('secondary-banners-block').classList.add('hidden');
            document.getElementById('static-content-block').classList.add('hidden');

            setActiveNav(`nav-${cat}`);
            updateSiloSEOStates();
            renderProductsGrid();
            showToast(`Đã vào Chuyên mục lớn: ${getCategoryNameVi(cat)}`, "📂");
        }

        // Lọc theo Chuyên mục con Cấp 2
        window.selectSubcategory = function(cat, sub) {
            currentSiloState = { level: 2, category: cat, subcategory: sub };
            filteredProducts = allProducts.filter(p => p.category === cat && p.subcategory === sub);
            
            // Ẩn các banner quảng cáo gây loãng thông tin khi lọc sâu
            document.getElementById('main-promo-banner').classList.add('hidden');
            document.getElementById('view-title-block').classList.remove('hidden');
            document.getElementById('products-grid').classList.remove('hidden');
            document.getElementById('secondary-banners-block').classList.add('hidden');
            document.getElementById('static-content-block').classList.add('hidden');

            setActiveNav(`nav-${cat}`);
            updateSiloSEOStates();
            renderProductsGrid();
            showToast(`Lọc sâu nhánh: ${getSubcategoryNameVi(sub)}`, "🌿");
        }

        // Khôi phục bộ lọc về mặc định ban đầu (Trang Chủ)
        window.resetFilters = function() {
            currentSiloState = { level: 0, category: 'all', subcategory: 'all' };
            filteredProducts = [...allProducts];
            
            document.getElementById('global-search').value = "";
            document.getElementById('view-title').innerHTML = `<i class="fa-solid fa-box-open text-rawRed-500"></i> Tất cả đồ nhựa & tủ nhựa gia dụng`;
            document.getElementById('view-description').textContent = "Duyệt và mua sắm các thiết bị tiện ích gia đình hàng đầu được RAW PLASTIC cam kết chất lượng chính hãng";

            // Hiện lại toàn bộ banner chào mừng của Trang Chủ
            document.getElementById('main-promo-banner').classList.remove('hidden');
            document.getElementById('view-title-block').classList.remove('hidden');
            document.getElementById('products-grid').classList.remove('hidden');
            document.getElementById('secondary-banners-block').classList.remove('hidden');
            document.getElementById('static-content-block').classList.add('hidden');

            setActiveNav('nav-home');
            updateSiloSEOStates();
            renderProductsGrid();
            showToast("Quay về trang chủ của RAW PLASTIC", "🏠");
        }

        // Cập nhật các chỉ số SEO HUD & Breadcrumbs dựa trên mức độ click
        function updateSiloSEOStates() {
            const depthBadge = document.getElementById('click-depth-badge');
            const juiceBadge = document.getElementById('link-juice-badge');
            const breadcrumb = document.getElementById('breadcrumb-container');
            const title = document.getElementById('view-title');
            const desc = document.getElementById('view-description');

            let breadcrumbHtml = `<span class="hover:text-rawRed-500 cursor-pointer" onclick="resetFilters()">Trang chủ</span>`;

            if (currentSiloState.level === 0) {
                depthBadge.textContent = "Độ sâu nhấp chuột: 0";
                juiceBadge.textContent = "Link Juice truyền: 100%";
                juiceBadge.className = "bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded text-[10px]";
                
                breadcrumb.innerHTML = breadcrumbHtml;
            } else if (currentSiloState.level === 1) {
                depthBadge.textContent = "Độ sâu nhấp chuột: 1";
                juiceBadge.textContent = "Link Juice truyền: 75%";
                juiceBadge.className = "bg-blue-100 text-blue-800 px-2.5 py-0.5 rounded text-[10px]";
                
                breadcrumbHtml += ` <span class="text-neutral-300">/</span> <span class="text-neutral-800 font-bold cursor-pointer" onclick="selectCategory('${currentSiloState.category}')">${getCategoryNameVi(currentSiloState.category)}</span>`;
                breadcrumb.innerHTML = breadcrumbHtml;

                title.textContent = `Chuyên mục chính: ${getCategoryNameVi(currentSiloState.category)}`;
                desc.textContent = `Danh sách đầy đủ các sản phẩm thuộc phân loại lớn ${getCategoryNameVi(currentSiloState.category)}.`;
            } else if (currentSiloState.level === 2) {
                depthBadge.textContent = "Độ sâu nhấp chuột: 2";
                juiceBadge.textContent = "Link Juice truyền: 50%";
                juiceBadge.className = "bg-amber-100 text-amber-800 px-2.5 py-0.5 rounded text-[10px]";

                breadcrumbHtml += ` <span class="text-neutral-300">/</span> <span class="text-neutral-500 cursor-pointer" onclick="selectCategory('${currentSiloState.category}')">${getCategoryNameVi(currentSiloState.category)}</span>`;
                breadcrumbHtml += ` <span class="text-neutral-300">/</span> <span class="text-neutral-800 font-bold">${getSubcategoryNameVi(currentSiloState.subcategory)}</span>`;
                breadcrumb.innerHTML = breadcrumbHtml;

                title.textContent = `${getSubcategoryNameVi(currentSiloState.subcategory)}`;
                desc.textContent = `Cụm từ khóa chuyên biệt đóng gói khép kín, tối ưu hóa sức mạnh công cụ tìm kiếm chuẩn SEO.`;
            }
        }

        // Render danh sách sản phẩm bán chạy có ảnh thu nhỏ bên trái
        function renderBestSellers() {
            const container = document.getElementById('best-sellers-list');
            const bestSellers = localBackupProducts.filter(p => p.badge === "Bán chạy").slice(0, 4);

            container.innerHTML = bestSellers.map(p => `
                <div class="flex items-center gap-3 py-2 text-xs">
                    <span class="text-2xl shrink-0 select-none bg-neutral-100 p-1.5 rounded-lg border border-neutral-200">${p.image}</span>
                    <div class="min-w-0 flex-grow">
                        <h4 onclick="sendQuickQuestion('Tư vấn sản phẩm ${p.name}')" class="font-extrabold text-neutral-800 truncate hover:text-rawRed-500 cursor-pointer" title="${p.name}">${p.name}</h4>
                        <div class="flex items-center gap-1.5 mt-1 font-semibold">
                            <span class="text-rawRed-500">${formatVND(p.price)}</span>
                            ${p.originalPrice ? `<span class="text-neutral-400 text-[10px] line-through">${formatVND(p.originalPrice)}</span>` : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Bật tắt Drawer giỏ hàng bên phải
        window.toggleCartDrawer = function() {
            const drawer = document.getElementById('cart-drawer');
            if (drawer.classList.contains('hidden')) {
                drawer.classList.remove('hidden');
                setTimeout(() => drawer.classList.remove('translate-x-full'), 10);
            } else {
                drawer.classList.add('translate-x-full');
                setTimeout(() => drawer.classList.add('hidden'), 300);
            }
        }

        // Thêm sản phẩm vào giỏ hàng
        window.addToCart = function(id) {
            const item = allProducts.find(p => p.id === id);
            if (!item) return;

            const existed = cart.find(p => p.id === id);
            if (existed) {
                existed.qty += 1;
            } else {
                cart.push({ ...item, qty: 1 });
            }

            saveCartToStorage();
            updateCartUI();
            showToast(`Đã thêm "${item.name}" vào giỏ hàng thành công!`, "🛒");
        }

        // Đọc lưu giỏ hàng
        function saveCartToStorage() {
            localStorage.setItem("raw_plastic_cart", JSON.stringify(cart));
        }

        function initCart() {
            const saved = localStorage.getItem("raw_plastic_cart");
            if (saved) {
                try {
                    cart = JSON.parse(saved);
                    updateCartUI();
                } catch (e) {
                    cart = [];
                }
            }
        }

        // Cập nhật giao diện giỏ hàng thời gian thực
        function updateCartUI() {
            const count = cart.reduce((acc, item) => acc + item.qty, 0);
            document.getElementById('top-cart-count').textContent = count;

            const container = document.getElementById('cart-items-container');
            if (cart.length === 0) {
                container.innerHTML = `
                    <div class="h-full flex flex-col items-center justify-center text-center text-neutral-400 py-16">
                        <span class="text-5xl mb-3">📦</span>
                        <p class="font-bold text-xs">Giỏ hàng rỗng</p>
                        <p class="text-[10px] text-neutral-500 mt-1">Vui lòng lựa chọn đồ gia dụng để thêm vào giỏ.</p>
                    </div>
                `;
                document.getElementById('cart-total').textContent = "0₫";
                return;
            }

            container.innerHTML = cart.map(item => `
                <div class="flex items-center gap-3 bg-neutral-50 p-2.5 rounded-xl border border-neutral-150">
                    <span class="text-3xl shrink-0 select-none bg-white p-2 rounded-lg border border-neutral-200">${item.image}</span>
                    <div class="flex-grow min-w-0 text-xs">
                        <h4 class="font-bold text-neutral-800 truncate" title="${item.name}">${item.name}</h4>
                        <p class="text-rawRed-500 font-extrabold mt-0.5">${formatVND(item.price)}</p>
                        <div class="flex items-center gap-1.5 mt-1.5">
                            <button onclick="changeQty(${item.id}, -1)" class="w-5 h-5 bg-white border border-neutral-300 rounded font-bold hover:bg-neutral-100 flex items-center justify-center">-</button>
                            <span class="font-bold text-neutral-700">${item.qty}</span>
                            <button onclick="changeQty(${item.id}, 1)" class="w-5 h-5 bg-white border border-neutral-300 rounded font-bold hover:bg-neutral-100 flex items-center justify-center">+</button>
                        </div>
                    </div>
                    <button onclick="removeFromCart(${item.id})" class="text-slate-400 hover:text-rawRed-500 p-2 text-sm">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            `).join('');

            const total = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
            document.getElementById('cart-total').textContent = formatVND(total);
        }

        // Tăng giảm số lượng sản phẩm
        window.changeQty = function(id, val) {
            const item = cart.find(p => p.id === id);
            if (!item) return;
            item.qty += val;
            if (item.qty <= 0) {
                removeFromCart(id);
                return;
            }
            saveCartToStorage();
            updateCartUI();
        }

        window.removeFromCart = function(id) {
            cart = cart.filter(p => p.id !== id);
            saveCartToStorage();
            updateCartUI();
        }

        // Quản lý Modal mua hàng & thanh toán VietQR
        window.openCheckoutModal = function() {
            if (cart.length === 0) {
                showToast("Giỏ hàng rỗng, vui lòng mua hàng", "⚠️");
                return;
            }
            const modal = document.getElementById('checkout-modal');
            const total = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
            
            document.getElementById('modal-total-amount').textContent = formatVND(total);
            document.getElementById('qr-total-amount').textContent = formatVND(total);
            modal.classList.remove('hidden');
        }

        window.closeCheckoutModal = function() {
            document.getElementById('checkout-modal').classList.add('hidden');
        }

        window.toggleQRDisplay = function(show) {
            const qrArea = document.getElementById('qr-payment-area');
            if (show) {
                qrArea.classList.remove('hidden');
            } else {
                qrArea.classList.add('hidden');
            }
        }

        // Form Gửi đặt hàng lưu trữ
        document.getElementById('order-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const customerName = document.getElementById('customer-name').value;
            const phone = document.getElementById('customer-phone').value;
            const address = document.getElementById('customer-address').value;
            const paymentMethod = document.querySelector('input[name="payment-method"]:checked').value;

            const totalAmount = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
            const items = cart.map(item => ({
                productId: item.id,
                name: item.name,
                price: item.price,
                quantity: item.qty
            }));

            const orderData = { customerName, phone, address, paymentMethod, items, totalAmount };

            try {
                if (isBackendConnected) {
                    const res = await fetch(`${API_BASE}/orders`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(orderData)
                    });
                    const data = await res.json();
                    if (data.success) {
                        showToast("Đơn hàng đã lưu thành công vào MongoDB!", "🎉");
                    } else {
                        throw new Error(data.message);
                    }
                } else {
                    console.log("Đặt hàng offline thành công:", orderData);
                    showToast("Đơn hàng của bạn đã đặt thành công (Offline)!", "🎉");
                }

                // Làm trống giỏ hàng
                cart = [];
                saveCartToStorage();
                updateCartUI();
                closeCheckoutModal();
                document.getElementById('order-form').reset();
            } catch (err) {
                showToast("Có lỗi xảy ra: " + err.message, "❌");
            }
        });

        // Tìm kiếm máy ảnh thời gian thực
        window.handleSearch = function(query) {
            const normalized = query.toLowerCase().trim();
            const suggestions = document.getElementById('search-suggestions');
            
            if (!normalized) {
                suggestions.classList.add('hidden');
                filteredProducts = [...allProducts];
                renderProductsGrid();
                return;
            }

            // Gợi ý danh sách nhỏ
            const matched = allProducts.filter(p => p.name.toLowerCase().includes(normalized));
            filteredProducts = matched;
            renderProductsGrid();

            if (matched.length > 0) {
                suggestions.classList.remove('hidden');
                suggestions.innerHTML = matched.slice(0, 5).map(p => `
                    <div onclick="clickSearchSuggestion('${p.name}')" class="px-4 py-2.5 hover:bg-neutral-100 text-xs text-neutral-800 font-semibold cursor-pointer flex items-center justify-between border-b border-neutral-100 last:border-none">
                        <span>${p.name}</span>
                        <span class="text-rawRed-500 font-extrabold">${formatVND(p.price)}</span>
                    </div>
                `).join('');
            } else {
                suggestions.innerHTML = `<div class="px-4 py-3 text-xs text-neutral-400 text-center">Không có sản phẩm nào phù hợp.</div>`;
            }
        }

        window.clickSearchSuggestion = function(name) {
            document.getElementById('global-search').value = name;
            document.getElementById('search-suggestions').classList.add('hidden');
            filteredProducts = allProducts.filter(p => p.name === name);
            renderProductsGrid();
        }

        // Tích hợp Trợ lý máy ảnh AI
        function setupAIChat() {
            const drawer = document.getElementById('ai-chat-drawer');
            const openBtn = document.getElementById('ai-trigger-btn');
            const closeBtn = document.getElementById('ai-chat-close-btn');
            const form = document.getElementById('ai-chat-form');

            openBtn.addEventListener('click', () => {
                drawer.classList.remove('hidden');
                setTimeout(() => drawer.classList.remove('translate-x-full'), 10);
            });

            closeBtn.addEventListener('click', () => {
                drawer.classList.add('translate-x-full');
                setTimeout(() => drawer.classList.add('hidden'), 300);
            });

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const input = document.getElementById('ai-input');
                const text = input.value.trim();
                if (!text) return;

                appendMsg("user", text);
                input.value = "";

                // Giả lập phân tích kỹ thuật
                setTimeout(() => {
                    const response = parseAIQuery(text);
                    appendMsg("bot", response);
                }, 850);
            });
        }

        window.sendQuickQuestion = function(text) {
            appendMsg("user", text);
            document.getElementById('ai-chat-drawer').classList.remove('hidden');
            setTimeout(() => {
                const response = parseAIQuery(text);
                appendMsg("bot", response);
            }, 850);
        }

        window.askAIAbooutProduct = function(name) {
            sendQuickQuestion(`Tư vấn thông số và cách dùng đối với ${name}`);
        }

        function appendMsg(role, text) {
            const container = document.getElementById('ai-messages-container');
            const isUser = role === "user";

            const div = document.createElement('div');
            div.className = `flex gap-2.5 items-start ${isUser ? 'flex-row-reverse' : ''}`;
            
            div.innerHTML = isUser ? `
                <span class="text-xl bg-neutral-100 p-2 rounded-xl shrink-0 select-none">👤</span>
                <div class="bg-neutral-900 text-white text-xs px-3.5 py-2.5 rounded-2xl max-w-[85%] leading-relaxed shadow">
                    ${text}
                </div>
            ` : `
                <span class="text-xl bg-rawRed-50 p-2 rounded-xl shrink-0 select-none">🤖</span>
                <div class="bg-neutral-50 text-slate-800 text-xs px-3.5 py-2.5 rounded-2xl max-w-[85%] leading-relaxed border border-neutral-100 shadow-sm space-y-2">
                    ${text}
                </div>
            `;

            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        // Phân tích từ khóa AI thông minh
        function parseAIQuery(query) {
            const q = query.toLowerCase();

            if (q.includes("tủ nhựa") || q.includes("duy tân") || q.includes("5 tầng")) {
                const p = localBackupProducts.find(x => x.id === 1); // Duy Tân Mina
                return `<strong>Tư vấn dòng tủ nhựa Duy Tân cao cấp:</strong><br><br>
                Bạn có thể tham khảo dòng tủ tốt nhất sau dành cho phòng ngủ hoặc đồ dùng trẻ sơ sinh:<br>
                - 📦 <strong>Tủ nhựa Duy Tân Mina 5 tầng 6 ngăn kéo</strong> (Giá ưu đãi: 1.450.000₫)<br>
                - Kích thước rộng rãi đựng nhiều quần áo gấp gọn, chất liệu nhựa nguyên sinh PP/ABS siêu bền, có tay nắm trơn tru an toàn tuyệt đối cho bé.<br><br>
                <button onclick="addToCart(${p.id})" class="bg-rawRed-500 hover:bg-rawRed-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold block mt-2 text-center">Mua Tủ Duy Tân Ngay</button>`;
            }

            if (q.includes("hộp") || q.includes("inochi") || q.includes("thực phẩm")) {
                const p = localBackupProducts.find(x => x.id === 9); // Bộ 3 hộp thực phẩm Inochi Hokkaido
                return `<strong>Bộ hộp đựng thực phẩm kháng khuẩn Inochi Nhật Bản:</strong><br><br>
                📍 <strong>Sản phẩm tiêu biểu:</strong><br>
                - 🍱 <em>Bộ 3 hộp nhựa thực phẩm Inochi Hokkaido</em> (129.000₫) - Tích hợp ion bạc kháng khuẩn tối ưu, chịu nhiệt trong lò vi sóng.<br><br>
                📍 <strong>Tính năng vượt trội:</strong><br>
                - Bảo quản thực phẩm luôn tươi ngon lâu hơn 30% so với hộp thông thường, không phôi màu dính độc hại ra thực phẩm.<br><br>
                <button onclick="addToCart(${p.id})" class="bg-rawRed-500 hover:bg-rawRed-600 text-white px-4 py-1.5 rounded-lg text-[10px] font-bold block mt-1.5 text-center">Thêm bộ 3 hộp Hokkaido vào giỏ</button>`;
            }

            if (q.includes("song long") || q.includes("gia dụng") || q.includes("ghế")) {
                const p = localBackupProducts.find(x => x.id === 18); // Bàn nhựa Song Long
                return `<strong>Các dòng sản phẩm nhựa gia dụng Song Long bền bỉ nhất:</strong><br><br>
                - 🪑 <strong>Ghế nhựa đẩu cao Song Long</strong> (45.000₫) - Tiện dụng dùng trong bếp ăn hoặc sân vườn.<br>
                - 🧱 <strong>Bàn nhựa mầm non Song Long</strong> (252.000₫) - Thiết kế vững chãi an toàn cho các bé học tập và vui chơi.<br><br>
                <button onclick="addToCart(${p.id})" class="bg-rawRed-500 hover:bg-rawRed-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold mt-2 block text-center">Mua Bàn Nhựa Song Long</button>`;
            }

            // Gợi ý mặc định
            return `Tôi hiểu câu hỏi của bạn. Tại <strong>RAW PLASTIC</strong>, chúng tôi cung cấp tủ nhựa Duy Tân, Song Long, hộp đựng thực phẩm Inochi chất lượng cao nhất. Bạn có thể nhấp chuột trực tiếp vào các nút danh mục bên trái hoặc liên hệ Skype/Zalo để được giải đáp tức thì!`;
        }

        setupAIChat();

        // Hiển thị nội dung trang tĩnh (Giới thiệu, Tin tức, Liên hệ)
        window.showStaticPage = function(page) {
            const grid = document.getElementById('products-grid');
            const staticBlock = document.getElementById('static-content-block');
            
            // Ẩn tất cả banner quảng cáo và danh mục khi xem trang tĩnh
            document.getElementById('main-promo-banner').classList.add('hidden');
            document.getElementById('view-title-block').classList.add('hidden');
            grid.classList.add('hidden');
            document.getElementById('secondary-banners-block').classList.add('hidden');
            staticBlock.classList.remove('hidden');

            setActiveNav(`nav-${page}`);

            if (page === 'about') {
                staticBlock.innerHTML = `
                    <div class="space-y-4">
                        <h2 class="text-xl font-bold text-rawRed-500 border-b border-neutral-100 pb-2">Về RAW PLASTIC SHOP</h2>
                        <p class="text-xs text-neutral-600 leading-relaxed">Được thành lập với mong muốn mang những thiết bị nhựa gia dụng thông minh và an toàn sức khỏe tới người dùng Việt Nam, RAW PLASTIC tự hào là đối tác phân phối ủy quyền lớn của các thương hiệu hàng đầu như Duy Tân, Song Long và thương hiệu phong cách Nhật Bản Inochi.</p>
                        <p class="text-xs text-neutral-600 leading-relaxed">Chúng tôi cam kết 100% sản phẩm phân phối ra thị trường là hàng chính hãng, đầy đủ hóa đơn kiểm định không chứa chất độc hại BPA, hỗ trợ dùng thử không ưng ý đổi trả dễ dàng trong vòng 15 ngày đầu tiên.</p>
                    </div>
                `;
            } else if (page === 'news') {
                staticBlock.innerHTML = `
                    <div class="space-y-4">
                        <h2 class="text-xl font-bold text-rawRed-500 border-b border-neutral-100 pb-2">Tin tức công nghệ đồ nhựa gia dụng</h2>
                        <div class="space-y-4 text-xs divide-y divide-neutral-100">
                            <div class="pt-3 first:pt-0">
                                <h4 class="font-extrabold text-neutral-900 text-sm">Chất liệu nhựa PP nguyên sinh tích hợp ion bạc là gì?</h4>
                                <p class="text-neutral-500 mt-1">Sự khác biệt vượt trội trong công nghệ kháng khuẩn giúp bảo quản thực phẩm của dòng sản phẩm Inochi được tin dùng hiện nay...</p>
                            </div>
                            <div class="pt-3">
                                <h4 class="font-extrabold text-neutral-900 text-sm">Cách chọn tủ nhựa đựng quần áo an toàn cho bé sơ sinh</h4>
                                <p class="text-neutral-500 mt-1">Lời khuyên từ các chuyên gia giúp mẹ bỉm lựa chọn tủ kéo của Duy Tân hoặc Song Long sao cho tiện dụng và không độc hại...</p>
                            </div>
                        </div>
                    </div>
                `;
            } else if (page === 'contact') {
                staticBlock.innerHTML = `
                    <div class="space-y-4">
                        <h2 class="text-xl font-bold text-rawRed-500 border-b border-neutral-100 pb-2">Thông tin liên hệ & Bảo hành</h2>
                        <p class="text-xs text-neutral-600">Quý khách vui lòng liên hệ thông tin chi tiết dưới đây để được hỗ trợ mua sắm hoặc bảo hành thiết bị nhanh nhất:</p>
                        <ul class="space-y-2 text-xs text-neutral-700">
                            <li><i class="fa-solid fa-location-dot text-rawRed-500 mr-2"></i> <strong>Địa chỉ Hà Nội:</strong> Tòa nhà Ladeco, 266 Đội Cấn, Quận Ba Đình, Hà Nội</li>
                            <li><i class="fa-solid fa-envelope text-rawRed-500 mr-2"></i> <strong>Email hỗ trợ:</strong> support@sapo.vn</li>
                            <li><i class="fa-solid fa-clock text-rawRed-500 mr-2"></i> <strong>Giờ làm việc:</strong> 8:00 - 21:30 hàng ngày</li>
                        </ul>
                    </div>
                `;
            }
            showToast(`Đang hiển thị trang: ${page === 'about' ? 'Giới thiệu' : page === 'news' ? 'Tin tức' : 'Liên hệ'}`, "ℹ️");
        }

        // Tên tiếng Việt phân loại
        function getCategoryNameVi(cat) {
            if (cat === 'cabinets') return "Tủ Nhựa Cao Cấp";
            if (cat === 'containers') return "Hộp & Khay Kháng Khuẩn";
            if (cat === 'houseware') return "Đồ Gia Dụng";
            return "Khác";
        }

        function getSubcategoryNameVi(sub) {
            if (sub === 'duytan_cabinets') return "Duy Tân Siêu Bền";
            if (sub === 'songlong_cabinets') return "Song Long Đa Sắc";
            if (sub === 'inochi_boxes') return "Hộp Nhựa Inochi";
            if (sub === 'utility_trays') return "Khay Nhựa Tiện Ích";
            if (sub === 'chairs_tables') return "Bàn Ghế Nhựa";
            if (sub === 'shelves_bins') return "Kệ & Thùng Rác";
            return "Khác";
        }

        // Custom Toast thông báo nhanh thay thế alert
        function showToast(message, icon = "⚡") {
            const toast = document.getElementById('toast');
            document.getElementById('toast-icon').textContent = icon;
            document.getElementById('toast-message').textContent = message;
            
            toast.className = "fixed bottom-10 left-1/2 -translate-x-1/2 z-50 transform translate-y-0 opacity-100 transition-all duration-300 pointer-events-auto";
            
            setTimeout(() => {
                toast.className = "fixed bottom-5 left-1/2 -translate-x-1/2 z-50 transform translate-y-10 opacity-0 transition-all duration-300 pointer-events-none";
            }, 3000);
        }

        // Hàm định dạng tiền tệ Việt Nam
        function formatVND(amount) {
            return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
        }
    </script>
</body>
</html>
