import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, Search, ClipboardList, Bot, 
  ChevronRight, X, FileUser, HeartPulse, LandPlot, 
  MapPin, Loader2, Globe, FileText
} from 'lucide-react';

const CATEGORY_INFO = {
  'Căn cước': { icon: <FileUser size={24}/>, desc: 'Giấy tờ tùy thân cốt lõi, xác định danh tính công dân. Việc sở hữu căn cước giúp thực hiện giao dịch dân sự, tài chính và dịch vụ công trực tuyến bảo mật, nhanh chóng.' },
  'Hộ tịch': { icon: <ClipboardList size={24}/>, desc: 'Bằng chứng pháp lý về tình trạng cá nhân (khai sinh, kết hôn, khai tử). Đảm bảo quyền và lợi ích hợp pháp của bạn trước pháp luật.' },
  'Đất đai': { icon: <LandPlot size={24}/>, desc: 'Xác lập quyền sở hữu, sử dụng tài sản nhà đất hợp pháp. Bảo vệ tài sản và dễ dàng thực hiện các giao dịch chuyển nhượng, thế chấp.' },
  'Y tế': { icon: <HeartPulse size={24}/>, desc: 'Tiếp cận chăm sóc sức khỏe. Thủ tục bảo hiểm y tế giúp giảm bớt gánh nặng chi phí và hưởng chế độ chăm sóc y tế toàn dân.' }
};

const PROCEDURES = [
  { id: 1, title: 'Cấp Căn cước công dân gắn chip', category: 'Căn cước', time: '7-10 ngày', documents: ['CCCD cũ (nếu có)', 'Giấy khai sinh/Sổ hộ khẩu (bản sao)', 'Thông tin cá nhân trên hệ thống QG'], steps: ['Đến cơ quan Công an', 'Thu nhận dữ liệu sinh trắc học', 'Đóng lệ phí', 'Nhận kết quả'], advice: 'Nên đặt lịch hẹn trước qua Cổng dịch vụ công để tránh chờ đợi lâu.' },
  { id: 2, title: 'Đăng ký kết hôn', category: 'Hộ tịch', time: '3-5 ngày', documents: ['CCCD 2 bên', 'Giấy xác nhận tình trạng hôn nhân', 'Tờ khai đăng ký kết hôn'], steps: ['Nộp hồ sơ tại UBND cấp xã', 'Xác minh thông tin', 'Ký sổ hộ tịch', 'Nhận giấy chứng nhận'], advice: 'Cả hai bên nam và nữ cần có mặt trực tiếp để ký tên.' },
  { id: 3, title: 'Đăng ký khai sinh', category: 'Hộ tịch', time: '1-3 ngày', documents: ['Giấy chứng sinh (bản gốc)', 'CCCD cha mẹ', 'Giấy đăng ký kết hôn'], steps: ['Chuẩn bị giấy chứng sinh', 'Nộp tại UBND xã/phường', 'Nhận giấy khai sinh'], advice: 'Nên thực hiện trong vòng 60 ngày kể từ ngày sinh để tránh bị phạt.' },
  { id: 6, title: 'Cấp đổi sổ đỏ', category: 'Đất đai', time: '15-20 ngày', documents: ['Sổ đỏ cũ', 'Hợp đồng chuyển nhượng', 'CCCD', 'Giấy tờ chứng minh nghĩa vụ tài chính'], steps: ['Đo đạc địa chính', 'Nộp hồ sơ tại Văn phòng đăng ký đất đai', 'Đóng thuế', 'Nhận sổ'], advice: 'Cần có sự đồng thuận của tất cả các đồng sở hữu.' },
  { id: 7, title: 'Cấp thẻ Bảo hiểm y tế', category: 'Y tế', time: '7 ngày', documents: ['Tờ khai TK1-TS', 'CCCD'], steps: ['Tờ khai TK1-TS', 'Nộp tại cơ quan BHXH hoặc đại lý', 'Nhận thẻ'], advice: 'Kiểm tra thông tin trên tờ khai thật kỹ trước khi nộp.' }
];

export default function App() {
  const [view, setView] = useState('home');
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Xin chào! Tôi là Trợ lý Hành Chính Thông. Tôi có thể tư vấn thủ tục hoặc tra cứu thông tin pháp luật giúp bạn.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProc, setSelectedProc] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { role: 'user', text: input }]);
    const query = input.toLowerCase();
    setInput('');
    setIsLoading(true);

    // 1. Check local DB first
    const found = PROCEDURES.find(p => p.title.toLowerCase().includes(query) || query.includes(p.title.toLowerCase()));
    
    if (found) {
        setMessages(prev => [...prev, { role: 'bot', text: `Tôi tìm thấy thủ tục chính thống trong hệ thống: "${found.title}".\n\n📌 Thời gian: ${found.time}\n📄 Hồ sơ: ${found.documents.join(', ')}\n✅ Các bước: ${found.steps.join(' -> ')}\n💡 Lời khuyên: ${found.advice}` }]);
        setIsLoading(false);
        return;
    }

    // 2. Fallback to Gemini + Search Tool
    try {
        const apiKey = ""; 
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`;
        
        const payload = {
            contents: [{ parts: [{ text: `Bạn là trợ lý hành chính chuyên nghiệp. Hãy trả lời câu hỏi sau về thủ tục hành chính tại Việt Nam: "${query}". Nếu cần, hãy tìm kiếm thông tin mới nhất trên internet.` }] }],
            tools: [{ "google_search": {} }],
            systemInstruction: { parts: [{ text: "Trả lời ngắn gọn, chuyên nghiệp, chính xác về thủ tục hành chính Việt Nam. Luôn ưu tiên đưa ra các bước cụ thể hoặc giấy tờ cần thiết." }] }
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        const botResponse = result.candidates[0].content.parts[0].text;
        setMessages(prev => [...prev, { role: 'bot', text: botResponse }]);
    } catch (error) {
        setMessages(prev => [...prev, { role: 'bot', text: "Hiện tại tôi đang gặp chút lỗi kết nối mạng. Bạn vui lòng thử lại hoặc tra cứu trực tiếp tại Cổng dịch vụ công Quốc gia." }]);
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <nav className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center gap-2 text-blue-700 font-bold text-xl cursor-pointer" onClick={() => setView('home')}>
            <ClipboardList /> Hành Chính Thông
          </div>
          <div className="flex gap-4 font-bold text-sm">
            <button onClick={() => setView('home')} className={view === 'home' ? 'text-blue-600' : 'text-gray-500'}>Trang chủ</button>
            <button onClick={() => setView('ai-chat')} className={view === 'ai-chat' ? 'text-blue-600' : 'text-gray-500'}>Tư vấn AI</button>
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-6xl mx-auto w-full p-4 md:p-8">
        {view === 'home' && (
          <div className="space-y-8">
            <h2 className="text-2xl font-bold">Danh mục thủ tục</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.keys(CATEGORY_INFO).map(cat => (
                <div key={cat} className="bg-white p-6 rounded-2xl border shadow-sm hover:shadow-md transition">
                  <div className="flex items-center gap-3 mb-4 text-blue-600">{CATEGORY_INFO[cat].icon} <h3 className="font-bold text-lg">{cat}</h3></div>
                  <p className="text-gray-600 text-sm mb-4">{CATEGORY_INFO[cat].desc}</p>
                  <ul className="space-y-2">
                    {PROCEDURES.filter(p => p.category === cat).map(p => (
                      <li key={p.id} onClick={() => setSelectedProc(p)} className="cursor-pointer text-blue-700 font-medium hover:underline text-sm flex items-center">
                        <ChevronRight size={14}/> {p.title}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}

        {view === 'ai-chat' && (
          <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-lg border h-[600px] flex flex-col">
            <div className="p-4 border-b font-bold bg-blue-50 rounded-t-2xl flex items-center gap-2"><Bot className="text-blue-600"/> Trợ lý AI (Có tra cứu mở rộng)</div>
            <div className="flex-1 p-4 overflow-y-auto space-y-4">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-3 rounded-2xl max-w-[80%] ${m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>{m.text}</div>
                </div>
              ))}
              {isLoading && <div className="text-sm text-gray-500 flex items-center gap-2"><Loader2 className="animate-spin"/> AI đang tra cứu...</div>}
              <div ref={chatEndRef} />
            </div>
            <div className="p-4 border-t flex gap-2">
              <input value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && handleSend()} className="flex-1 p-3 border rounded-full outline-none" placeholder="Hỏi tôi bất cứ thủ tục nào..." />
              <button onClick={handleSend} className="bg-blue-600 text-white p-3 rounded-full"><Send size={20}/></button>
            </div>
          </div>
        )}
      </main>

      {selectedProc && (
        <div className="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl w-full max-w-lg p-6 max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4"><h3 className="font-bold text-xl">{selectedProc.title}</h3> <button onClick={() => setSelectedProc(null)}><X/></button></div>
            <div className="space-y-4 text-sm">
              <p><strong>Thời gian:</strong> {selectedProc.time}</p>
              <div><strong>Hồ sơ cần mang:</strong> <ul className="list-disc pl-4">{selectedProc.documents.map((d, i) => <li key={i}>{d}</li>)}</ul></div>
              <div><strong>Các bước:</strong> <ol className="list-decimal pl-4">{selectedProc.steps.map((s, i) => <li key={i}>{s}</li>)}</ol></div>
              <p className="bg-yellow-50 p-3 rounded text-yellow-800"><strong>Lời khuyên:</strong> {selectedProc.advice}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
