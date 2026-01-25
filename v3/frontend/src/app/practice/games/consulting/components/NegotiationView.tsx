import React from 'react';

export default function NegotiationView() {
    return (
        <div className="h-full flex gap-4 p-4 overflow-hidden">

            {/* Chat List (Sidebar) */}
            <div className="w-1/3 glass-card rounded-xl flex flex-col overflow-hidden border border-white/5">
                <div className="p-4 border-b border-white/5">
                    <h2 className="text-sm font-bold uppercase tracking-widest text-gray-400">Active Comms</h2>
                </div>
                <div className="flex-1 overflow-y-auto">
                    <ChatItem name="Arasaka Corp" role="Client" status="active" message="We need to discuss the timeline..." time="2m ago" active />
                    <ChatItem name="Militech" role="Vendor" status="offline" message="Offer accepted." time="4h ago" />
                    <ChatItem name="Kang Tao" role="Client" status="away" message="Sending the updated specs." time="1d ago" />
                </div>
            </div>

            {/* Chat Area */}
            <div className="w-2/3 glass-card rounded-xl flex flex-col border border-white/5 overflow-hidden">
                {/* Header */}
                <div className="p-4 border-b border-white/5 flex justify-between items-center bg-white/5">
                    <div>
                        <h3 className="font-bold text-white">Arasaka Corp</h3>
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                            <span className="text-[10px] text-green-400 font-mono uppercase">Negotiation in progress</span>
                        </div>
                    </div>
                    <div className="text-right text-xs">
                        <p className="text-gray-400">Contract Value</p>
                        <p className="text-[var(--accent-gold)] font-mono font-bold">12,500 C</p>
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-4 bg-black/20">
                    <Message sender="them" text="The proposed budget for the Japan expansion seems high. Can we optimize the operational costs?" time="10:30 AM" />
                    <Message sender="me" text="Given the requirement for local compliance experts, the cost is justified. However, we can reduce the travel budget if we use remote workshops." time="10:32 AM" />
                    <Message sender="them" text="Remote workshops... That might work. What is the impact on the timeline?" time="10:33 AM" />
                </div>

                {/* Input */}
                <div className="p-4 border-t border-white/5 bg-white/5">
                    <div className="flex gap-2">
                        <input type="text" placeholder="Type your response..." className="flex-1 bg-black/40 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:border-[var(--accent-blue)] outline-none transition" />
                        <button className="bg-[var(--accent-blue)] text-black font-bold px-6 py-2 rounded-lg hover:brightness-110 transition"><i className="fa-solid fa-paper-plane"></i></button>
                    </div>
                    <p className="text-[9px] text-gray-500 mt-2 text-center">AI Client Patience: <span className="text-green-400">85%</span></p>
                </div>
            </div>
        </div>
    );
}

function ChatItem({ name, role, message, time, status, active }: any) {
    return (
        <div className={`p-4 border-b border-white/5 cursor-pointer hover:bg-white/5 transition flex gap-3 ${active ? 'bg-white/5 border-l-2 border-l-[var(--accent-blue)]' : ''}`}>
            <div className="relative">
                <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-gray-300 font-bold overflow-hidden">
                    <img src={`https://ui-avatars.com/api/?name=${name}&background=random`} alt={name} />
                </div>
                <div className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-[#1e1e2d] ${status === 'active' ? 'bg-green-500' : status === 'offline' ? 'bg-gray-500' : 'bg-yellow-500'}`}></div>
            </div>
            <div className="flex-1 min-w-0">
                <div className="flex justify-between mb-1">
                    <h4 className={`text-sm font-bold truncate ${active ? 'text-white' : 'text-gray-300'}`}>{name}</h4>
                    <span className="text-[10px] text-gray-500">{time}</span>
                </div>
                <p className="text-xs text-gray-400 truncate">{message}</p>
            </div>
        </div>
    )
}

function Message({ sender, text, time }: any) {
    const isMe = sender === 'me';
    return (
        <div className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-3 text-sm ${isMe
                    ? 'bg-[var(--accent-blue)] text-black rounded-tr-none'
                    : 'bg-white/10 text-gray-200 rounded-tl-none border border-white/5'
                }`}>
                {text}
            </div>
            <span className="text-[9px] text-gray-500 mt-1 px-1">{time}</span>
        </div>
    )
}
