import React, { useEffect, useRef, useState } from 'react';

function Journal({ userId }) {
  const [content, setContent] = useState('');
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(`ws://localhost:8000/ws/${userId}`);

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'init' || data.type === 'update') {
        setContent(data.text);
      }
    };

    ws.current.onclose = () => console.log("WebSocket disconnected");
    return () => ws.current.close();
  }, [userId]);

  const handleChange = (e) => {
    const text = e.target.value;
    setContent(text);
    ws.current.send(JSON.stringify({ type: 'update', text }));
  };

  return (
    <textarea
      value={content}
      onChange={handleChange}
      rows="20"
      cols="80"
      style={{ width: '100%', fontSize: '1rem' }}
    />
  );
}

export default Journal;
