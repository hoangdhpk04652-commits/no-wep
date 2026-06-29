import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, Search, ClipboardList, Bot, 
  ChevronRight, ChevronLeft, FileUser, HeartPulse, LandPlot, 
  MapPin, Loader2, Globe
} from 'lucide-react';

const CATEGORY_INFO = {
  'Căn cước': { icon: <FileUser size={24}/>, desc: 'Giấy tờ tùy thân cốt lõi, xác định danh tính công dân. Việc sở hữu căn cước gắn chip giúp thực hiện các giao dịch dân sự, tài chính và dịch vụ công trực tuyến một cách bảo mật và nhanh chóng.' },
  'Hộ tịch': { icon: <ClipboardList size={24}/>, desc: 'Hộ tịch là bằng chứng pháp lý về tình trạng cá nhân (khai sinh, kết hôn, khai tử). Việc thực hiện đúng thủ tục hộ tịch là nền tảng để bảo đảm quyền và lợi ích hợp pháp của bạn trước pháp luật.' },
  'Đất đai': { icon: <LandPlot size={24}/>, desc: 'Thủ tục đất đai giúp xác lập quyền sở hữu, sử dụng tài sản nhà đất hợp pháp. Việc đăng ký đúng quy định giúp bạn bảo vệ tài sản, dễ dàng thực hiện các giao dịch chuyển nhượng, thế chấp an toàn.' },
  'Y tế': { icon: <HeartPulse size={24}/>, desc: 'Hệ thống y tế công bảo đảm quyền tiếp cận chăm sóc sức khỏe. Thủ tục bảo hiểm y tế giúp giảm bớt gánh nặng chi phí và đảm bảo bạn được hưởng đầy đủ các chế độ chăm sóc y tế toàn dân.' }
};

const INITIAL_PROCEDURES = [
  { id: 1, title: 'Cấp Căn cước công dân gắn chip', category: 'Căn cước', time: '7-10 ngày', documents: ['CCCD cũ (nếu có)', 'Giấy khai sinh/Sổ hộ khẩu (bản sao)', 'Thông tin cá nhân trên hệ thống QG'], steps: ['Đến cơ quan Công an', 'Thu nhận dữ liệu sinh trắc học', 'Đóng lệ phí', 'Nhận kết quả'], advice: 'Nên đặt lịch hẹn trước qua Cổng dịch vụ công để tránh phải chờ đợi lâu.' },
  { id: 2, title: 'Đăng ký kết hôn', category: 'Hộ tịch', time: '3-5 ngày', documents: ['CCCD 2 bên', 'Giấy xác nhận tình trạng hôn nhân', 'Tờ khai đăng ký kết hôn'], steps: ['Nộp hồ sơ tại UBND cấp xã', 'Xác minh thông tin', 'Ký sổ hộ tịch', 'Nhận giấy chứng nhận'], advice: 'Cả hai bên nam và nữ cần có mặt trực tiếp để ký tên.' },
  { id: 3, title: 'Đăng ký khai sinh', category: 'Hộ tịch', time: '1-3 ngày', documents: ['Giấy chứng sinh (bản gốc)', 'CCCD cha mẹ', 'Giấy đăng ký kết hôn'], steps: ['Chuẩn bị giấy chứng sinh', 'Nộp tại UBND xã/phường', 'Nhận giấy khai sinh'], advice: 'Nên thực hiện trong vòng 60 ngày kể từ ngày sinh để tránh bị phạt.' },
  { id: 6, title: 'Cấp đổi sổ đỏ (Giấy chứng nhận QSDĐ)', category: 'Đất đai', time: '15-20 ngày', documents: ['Sổ đỏ cũ', 'Hợp đồng chuyển nhượng', 'CCCD', 'Giấy tờ chứng minh nghĩa vụ tài chính'], steps: ['Đo đạc địa chính', 'Nộp hồ sơ tại Văn phòng đăng ký đất đai', 'Đóng thuế', 'Nhận sổ'], advice: 'Cần có sự đồng thuận của tất cả các đồng sở hữu.' },
  { id: 7, title: 'Cấp thẻ Bảo hiểm y tế', category: 'Y tế', time: '7 ngày', documents: ['Tờ khai TK1-TS', 'CCCD'], steps: ['Tờ khai TK1-TS', 'Nộp tại cơ quan BHXH hoặc đại lý', 'Nhận thẻ'], advice: 'Kiểm tra thông tin trên tờ khai thật kỹ trước khi nộp.' }
];

const normalizeString = (str) => {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
};

export default function App() {
  const [view, setView] = useState('home');
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Xin chào! Tôi là Trợ lý Hành Chính Thông. Tôi có thể tư vấn thủ tục có sẵn hoặc tra cứu thông tin mới nhất trên Internet giúp bạn.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProcedure, setSelectedProcedure] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    const normalizedQuery = normalizeString(input);
    const found = INITIAL_PROCEDURES.find(p => 
      normalizeString(p.title).includes(normalizedQuery) || 
      normalizedQuery.includes(normalizeString(p.title).split(' ')[0])
    );

    if (found) {
      setMessages(prev => [...prev, { 
        role: 'bot', 
        text: `Tôi tìm thấy thủ tục trong cơ sở dữ liệu: "${found.title}".\n\n- Thời gian: ${found.time}.\n- Hồ sơ: ${found.documents.join(', ')}.\n- Bước thực hiện: ${found.steps.join(' -> ')}.\n- Lời khuyên: ${found.advice}` 
      }]);
    } else {
      try {
        const payload = {
            contents: [{ parts: [{ text: `Tư vấn thủ tục hành chính tại Việt Nam: ${input}` }] }],
            tools: [{ "google_search": {} }],
            systemInstruction: {
                parts: [{ text: "Bạn là chuyên gia tư vấn hành chính công tại Việt Nam. Nếu thông tin không có trong danh sách thủ tục, hãy tìm kiếm trên Google để trả lời chính xác, ngắn gọn và dẫn nguồn (nếu có)." }]
            }
        };

        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=`;
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        const botResponse = result.candidates?.[0]?.content?.parts?.[0]?.text || "Xin lỗi, tôi không tìm thấy thông tin cụ thể cho yêu cầu này trên Internet. Bạn hãy kiểm tra lại từ khóa nhé!";
        
        setMessages(prev => [...prev, { role: 'bot', text: botResponse, isExternal: true }]);
      } catch (error) {
        setMessages(prev => [...prev, { role: 'bot', text: "Đã xảy ra lỗi kết nối. Vui lòng thử lại sau." }]);
      }
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center gap-2 text-blue-700 font-bold text-xl cursor-pointer" onClick={() => setView('home')}>
            <ClipboardList size={28} />
            <span>Hành Chính Thông</span>
          </div>
          <div className="flex gap-4 font-medium text-sm">
            <button onClick={() => setView('home')} className={view === 'home' ? 'text-blue-600' : 'text-gray-600'}>Trang chủ</button>
            <button onClick={() => setView('ai-chat')} className={view === 'ai-chat' ? 'text-blue-600' : 'text-gray-600'}>Tư vấn AI</button>
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-6xl mx-auto w-full p-4 md:p-8">
        {view === 'home' && (
          <div className="space-y-8">
            <section className="bg-blue-700 text-white p-8 rounded-2xl shadow-lg">
              <h1 className="text-3xl font-bold mb-4">Chào mừng đến với Hành Chính Thông</h1>
              <p>Hệ thống tư vấn thông minh, hỗ trợ tra cứu và tìm kiếm thông tin hành chính toàn diện.</p>
            </section>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
               {Object.keys(CATEGORY_INFO).map(cat => (
                 <div key={cat} className="bg-white p-6 rounded-xl border shadow-sm">
                    <div className="flex items-center gap-3 mb-2 text-blue-600">
                        {CATEGORY_INFO[cat].icon}
                        <h3 className="font-bold text-lg">{cat}</h3>
                    </div>
                    <p className="text-sm text-gray-600">{CATEGORY_INFO[cat].desc}</p>
                 </div>
               ))}
            </div>
          </div>
        )}

        {view === 'ai-chat' && (
          <div className="h-[500px] flex flex-col bg-white rounded-2xl shadow-xl overflow-hidden border max-w-2xl mx-auto">
            <div className="bg-blue-600 text-white p-4 font-bold flex items-center gap-2">
                <Bot size={20}/> Hành Chính Bot (Tìm kiếm AI)
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] p-3 rounded-2xl ${m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border shadow-sm'}`}>
                    {m.isExternal && <Globe size={14} className="inline mr-1 text-blue-500"/>}
                    {m.text}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start"><div className="bg-white p-3 rounded-2xl border shadow-sm flex items-center gap-2"><Loader2 className="animate-spin text-blue-600" size={16}/> Đang tra cứu thông tin...</div></div>
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="p-4 border-t flex gap-2">
              <input value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSend()} className="flex-1 p-3 border rounded-full outline-none" placeholder="Hỏi tôi bất cứ thủ tục gì..." />
              <button onClick={handleSend} disabled={isLoading} className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 disabled:opacity-50"><Send size={20} /></button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
