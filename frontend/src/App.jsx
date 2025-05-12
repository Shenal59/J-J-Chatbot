import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { ChatBubbleLeftRightIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline';

export default function App() {
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState('');
  const [sid, setSid] = useState(null);
  const endRef = useRef();

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/welcome')
      .then(resp => {
        setSid(resp.data.sid);
        setMsgs([{ text: resp.data.answer, isUser: false }]);
      })
      .catch(err => {
        console.error('Welcome load failed', err);
      });
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [msgs]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;
    
    const user = { text: input, isUser: true };
    const payload = {question: input,session_id: sid};
    setMsgs(m => [...m, user]);
    setInput('');
    try {
      const { data } = await axios.post('http://127.0.0.1:8000/chat', payload);
      const bot = { text: data.answer, isUser: false };
      setSid(data.session_id);
      setMsgs(m => [...m, bot]);
    } catch {
      setMsgs(m => [...m, { text: '⚠️ Error, please try again.', isUser: false }]);
    }
  }

  return (
    // Main BG
    <div className="
          min-h-screen 
          flex items-center justify-center
          bg-gradient-to-br from-blue-700 via-blue-400 to-gray-200 
          p-4">
      {/* Chat Box */}
      <div className="
            w-11/12 md:w-3/4 lg:w-1/4 
            h-[80vh] 
            flex flex-col 
            bg-white rounded-3xl shadow-xl overflow-hidden">
        {/* Header */}
        <header className="
                  flex items-center px-6 py-4 
                  bg-gradient-to-r 
                  from-gray-400 to-gray-300 text-blue-600">
          <ChatBubbleLeftRightIcon className="
                                    w-8 h-8 mr-2" />
          <h1 className="text-xl font-semibold">Lens4U Chat</h1>
        </header>

        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-200">
          {msgs.map((m,i) => (
            <div key={i} className={`flex ${m.isUser ? 'justify-end' : 'justify-start'}`}>
              <div className={`
                relative
                max-w-[80%] px-5 py-3
                ${m.isUser
                  ? 'bg-white text-gray-900 rounded-tl-2xl rounded-bl-2xl rounded-tr-xl'
                  : 'bg-white text-gray-900 rounded-tr-2xl rounded-br-2xl rounded-tl-xl'}
                shadow-md
              `}>
                {m.text}
                <span className={`
                  absolute bottom-0 ${m.isUser ? '-right-2' : '-left-2'}
                  w-3 h-3 bg-inherit
                  ${m.isUser ? 'rounded-l-full' : 'rounded-r-full'}
                `} />
              </div>
            </div>
          ))}
          <div ref={endRef} />
        </div>

        <form onSubmit={sendMessage} className="
                                      flex items-center p-4 
                                      bg-white border-t 
                                      border-gray-200">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your message…"
            className="
              flex-1 py-2 px-4
              border-2 border-gray-300 rounded-full
              focus:outline-full focus:outline-gray-500
            "
          />
          <button
            type="submit"
            className="
              ml-3 bg-blue-300 text-black p-3 rounded-full
              hover:bg-accent-600 transition
            "
            disabled={!input.trim()}
          >
            <PaperAirplaneIcon className="w-5 h-5 transform rotate-0" />
          </button>
        </form>
      </div>
    </div>
  );
}
