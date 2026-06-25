import React, { useState, useMemo } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, LineChart, Line, Cell } from 'recharts';

const App = () => {
  const [data, setData] = useState([]);
  
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const rows = event.target.result.split(/\r?\n/).filter(r => r.trim() !== "");
        const headers = ["Detail_ID", "Invoice_ID", "Customer_ID", "Order_Date", "Store_Location", "Payment_Method", "Product_ID", "Product_Name", "Category", "Quantity", "Cost_Price", "Sale_Price", "Invoice_Total", "Discount"];
        
        const parsedData = rows.slice(1).map(row => {
          // Xử lý linh hoạt hơn với nhiều dấu phân cách
          const values = row.split(/[\t,;|]+/); 
          let obj = {};
          headers.forEach((h, i) => obj[h] = (values[i] || "").trim());
          return obj;
        }).filter(item => item.Invoice_ID);
        setData(parsedData);
      } catch (err) {
        console.error("Lỗi xử lý tệp:", err);
      }
    };
    reader.readAsText(file);
  };

  const analysis = useMemo(() => {
    if (data.length === 0) return null;
    
    const values = data.map(d => parseFloat(d.Invoice_Total?.replace(/[^0-9.]/g, '')) || 0);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    
    const hourly = {}, products = {}, regions = {};
    data.forEach(d => {
      // Trích xuất giờ an toàn bằng Regex thay vì Date object
      const hMatch = d.Order_Date?.match(/(\d{1,2}):/);
      const h = hMatch ? parseInt(hMatch[1]) : 0;
      
      hourly[h] = (hourly[h] || 0) + (parseFloat(d.Invoice_Total) || 0);
      
      const name = d.Product_Name?.substring(0, 12) || "Khác";
      products[name] = (products[name] || 0) + (parseInt(d.Quantity) || 0);
      regions[d.Store_Location || "Chưa xác định"] = (regions[d.Store_Location] || 0) + 1;
    });

    return { 
      totalRows: data.length, mean: mean.toFixed(2),
      hourly: Object.entries(hourly).map(([h, v]) => ({h: `${h}h`, v: v.toFixed(0)})).sort((a,b) => parseInt(a.h) - parseInt(b.h)),
      products: Object.entries(products).map(([name, val]) => ({name, val})).sort((a,b) => b.val - a.val).slice(0,5),
      regions: Object.entries(regions).map(([name, val]) => ({name, val}))
    };
  }, [data]);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-6 text-blue-900">Báo cáo Phân tích Dữ liệu Bán hàng</h1>
      <input type="file" onChange={handleFileUpload} className="mb-6 p-2 bg-white border rounded" />

      {analysis ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 bg-white shadow rounded border">
            <h2 className="font-bold mb-2">1. Tổng quan số liệu</h2>
            <p>Tổng số đơn hàng: <span className="font-bold">{analysis.totalRows}</span></p>
            <p>Trung bình doanh thu/đơn: <span className="font-bold">{analysis.mean} VND</span></p>
          </div>
          
          <div className="p-4 bg-white shadow rounded border">
            <h2 className="font-bold mb-2">2. Doanh thu theo giờ (VND)</h2>
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={analysis.hourly}>
                <XAxis dataKey="h"/><Tooltip formatter={(v) => `${v} VND`}/><Line dataKey="v" stroke="#8884d8" strokeWidth={2}/>
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="p-4 bg-white shadow rounded border">
            <h2 className="font-bold mb-2">3. Top 5 sản phẩm (Số lượng)</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={analysis.products} margin={{ bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" fontSize={10}/>
                <YAxis/><Tooltip formatter={(v) => `${v} sản phẩm`}/>
                <Bar dataKey="val" fill="#82ca9d">
                  {analysis.products.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="p-4 bg-white shadow rounded border">
            <h2 className="font-bold mb-2">4. Phân bổ vùng miền (Đơn hàng)</h2>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={analysis.regions} dataKey="val" nameKey="name" label={(entry) => `${entry.name}: ${entry.val}`}>
                  {analysis.regions.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <Tooltip/>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      ) : (
        <div className="text-gray-500 italic p-4">Vui lòng tải tệp dữ liệu để bắt đầu phân tích...</div>
      )}
    </div>
  );
};
export default App;
