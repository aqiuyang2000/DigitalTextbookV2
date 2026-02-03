// FILE: D:\projects\singlepage\hotspot_editor\templates\shared_assets\js\hotspot-enhancer.js (FINALIZED WITH ICON COLOR FIX)

(function () {
  "use strict";

  if (typeof React === "undefined" || typeof ReactDOM === "undefined") {
    console.error("Hotspot Enhancer Error: React or ReactDOM is not loaded.");
    return;
  }

  const controlIconSize = window.APP_CONFIG?.controlIconSize || 24;
  const iconSizeStyle = { width: `${controlIconSize}px`, height: `${controlIconSize}px` };

  // --- *** 核心修改 1/2: 为 CloseIcon 的样式对象添加明确的颜色 *** ---
  const closeIconStyle = { ...iconSizeStyle, color: 'white' };
  // --- *** 修改结束 *** ---

  const { useState, useRef, useEffect, useCallback, memo } = React;

  const PlayIcon = memo(({ style }) => (<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style={style}><path fillRule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.647c1.295.742 1.295 2.545 0 3.286L7.279 20.99c-1.25.717-2.779-.217-2.779-1.643V5.653z" clipRule="evenodd" /></svg>));
  const PauseIcon = memo(({ style }) => (<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style={style}><path fillRule="evenodd" d="M6.75 5.25a.75.75 0 01.75.75v12a.75.75 0 01-1.5 0V6a.75.75 0 01.75-.75zM16.5 5.25a.75.75 0 01.75.75v12a.75.75 0 01-1.5 0V6a.75.75 0 01.75-.75z" clipRule="evenodd" /></svg>));
  const CloseIcon = memo(({ style }) => (<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style={style}><path fillRule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clipRule="evenodd" /></svg>));
  const VolumeHighIcon = memo(({style}) => (<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style={style}><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.318.664-2.66 1.905A9.76 9.76 0 001.5 12c0 .898.121 1.768.35 2.595.341 1.24 1.518 1.905 2.66 1.905H6.44l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06zM18.584 14.828a.75.75 0 001.06-1.06l-1.5-1.5a.75.75 0 00-1.06 1.06l1.5 1.5zm-2.25-2.25a.75.75 0 001.06-1.06l-1.5-1.5a.75.75 0 00-1.06 1.06l1.5 1.5z" /></svg>));
  const VolumeLowIcon = memo(({style}) => (<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style={style}><path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.318.664-2.66 1.905A9.76 9.76 0 001.5 12c0 .898.121 1.768.35 2.595.341 1.24 1.518 1.905 2.66 1.905H6.44l4.5 4.5c.944.945 2.56.276 2.56-1.06V4.06z" /></svg>));
  const MaximizeIcon = memo(({ style }) => (<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" style={style}><path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M20.25 20.25v-4.5m0 4.5h-4.5m4.5 0L15 15m-6 0l-3.75 3.75m0 0v-4.5m0 4.5h4.5m0-4.5l-3.75-3.75M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9" /></svg>));
  const MinimizeIcon = memo(({ style }) => (<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" style={style}><path strokeLinecap="round" strokeLinejoin="round" d="M9 9V4.5M9 9H4.5M9 9L3.75 3.75M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 9V4.5M15 9h4.5M15 9l5.25-5.25M15 15v4.5M15 15h4.5M15 15l5.25 5.25" /></svg>));

  const formatTime = (timeInSeconds) => { if (isNaN(timeInSeconds) || timeInSeconds < 0) return "0:00"; const minutes = Math.floor(timeInSeconds / 60); const seconds = Math.floor(timeInSeconds % 60); return `${minutes}:${seconds.toString().padStart(2, "0")}`; };

  const ModalPlayer = ({ item, isVisible, onClose }) => {
    if (!item) return null;
    const { url, origin, mediaType, description, aspectRatio } = item;
    const isVideo = mediaType === 'video' || mediaType === 'video_url';
    const getPlayerStyle = () => { const maxWidth = item.popupWidth ? parseInt(item.popupWidth, 10) : window.innerWidth * 0.8; const maxHeight = item.popupHeight ? parseInt(item.popupHeight, 10) : window.innerHeight * 0.8; if (aspectRatio && aspectRatio !== 'free') { const [ratioW, ratioH] = aspectRatio.split(':').map(Number); let width = maxWidth; let height = width * (ratioH / ratioW); if (height > maxHeight) { height = maxHeight; width = height * (ratioW / ratioH); } return { width: `${width}px`, height: `${height}px` }; } return { width: `${maxWidth}px`, height: `${maxHeight}px` }; };
    const [isMaximized, setIsMaximized] = useState(false);
    const size = getPlayerStyle();
    const playerContainerStyle = isMaximized ? { width: '100%', height: '100%', borderRadius: '0' } : { ...size, borderRadius: '0.5rem' };
    const aspectRatioClass = aspectRatio && aspectRatio !== 'free' ? `aspect-ratio-${aspectRatio.replace(':', '-')}` : '';
    const videoRef = useRef(null);
    const controlsTimeoutRef = useRef(null);
    const speedControlRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(true);
    const [progress, setProgress] = useState(0);
    const [duration, setDuration] = useState(0);
    const [volume, setVolume] = useState(1);
    const [playbackRate, setPlaybackRate] = useState(1);
    const [showControls, setShowControls] = useState(true);
    const [showSpeedOptions, setShowSpeedOptions] = useState(false);
    const [isClosing, setIsClosing] = useState(false);
    const handleClose = useCallback(() => { setIsClosing(true); setTimeout(onClose, 500); }, [onClose]);
    const animationContainerStyle = { transformOrigin: `${origin.x}px ${origin.y}px`, clipPath: isVisible && !isClosing ? `circle(142vmax at ${origin.x}px ${origin.y}px)` : `circle(0px at ${origin.x}px ${origin.y}px)`, opacity: isVisible && !isClosing ? 1 : 0, };
    const handleTogglePlay = () => { if (videoRef.current) { videoRef.current.paused ? videoRef.current.play() : videoRef.current.pause(); setIsPlaying(!videoRef.current.paused); }};
    const handleProgressChange = (e) => { const newTime = e.target.value * duration; if(videoRef.current) videoRef.current.currentTime = newTime; setProgress(e.target.value);};
    const handleVolumeChange = (e) => { const newVolume = parseFloat(e.target.value); if(videoRef.current) videoRef.current.volume = newVolume; setVolume(newVolume);};
    const handlePlaybackRateChange = (rate) => { if(videoRef.current) videoRef.current.playbackRate = rate; setPlaybackRate(rate); setShowSpeedOptions(false);};
    const hideControls = () => { if (isPlaying) setShowControls(false); };
    const handleMouseMove = () => { setShowControls(true); clearTimeout(controlsTimeoutRef.current); controlsTimeoutRef.current = setTimeout(hideControls, 3000);};
    useEffect(() => { const v = videoRef.current; if (!v) return; const up = () => setProgress(v.currentTime / v.duration); const ud = () => setDuration(v.duration); v.addEventListener('timeupdate', up); v.addEventListener('loadedmetadata', ud); return () => { v.removeEventListener('timeupdate', up); v.removeEventListener('loadedmetadata', ud); clearTimeout(controlsTimeoutRef.current); } }, []);
    useEffect(() => { if (isPlaying) { controlsTimeoutRef.current = setTimeout(hideControls, 3000); } else { clearTimeout(controlsTimeoutRef.current); setShowControls(true); }}, [isPlaying]);
    useEffect(() => { const h = (e) => { if (speedControlRef.current && !speedControlRef.current.contains(e.target)) { setShowSpeedOptions(false); }}; if (showSpeedOptions) { document.addEventListener('mousedown', h); } return () => { document.removeEventListener('mousedown', h); }; }, [showSpeedOptions]);
    const renderMedia = () => {
        switch (mediaType) {
            case 'video': case 'video_url': return <video ref={videoRef} src={url} autoPlay onClick={handleTogglePlay} />;
            case 'image': return <img src={url} alt={description} />;
            case 'pdf': case 'link': return <iframe src={url} title={description} sandbox="allow-scripts allow-same-origin allow-popups allow-forms"/>;
            default: return <div style={{color: '#fff'}}>Unsupported media type</div>;
        }
    };

    return ReactDOM.createPortal(
      <div className="enhancer-modal-overlay" onClick={handleClose}>
        <div className="enhancer-modal-animation-container" style={animationContainerStyle}>
          <div className="enhancer-modal-content-wrapper">
            <div className={`enhancer-modal-content ${aspectRatioClass}`} style={{...playerContainerStyle, backgroundColor: isVideo ? '#000' : '#fff' }} onClick={(e) => e.stopPropagation()} onMouseMove={isVideo ? handleMouseMove : null}>
              {renderMedia()}
              {isVideo && (
                 <div className="enhancer-video-controls-bg" style={{ opacity: showControls ? 1 : 0 }}>
                    <input type="range" min="0" max="1" step="0.001" value={progress || 0} onChange={handleProgressChange} />
                    <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '0.5rem'}}>
                        {/* --- *** 核心修改 2/2: 应用 closeIconStyle *** --- */}
                        <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}><button onClick={handleClose} title="Close" style={{background:'none', border:'none', color:'white', cursor:'pointer'}}><CloseIcon style={closeIconStyle} /></button><button onClick={handleTogglePlay} style={{background:'none', border:'none', color:'white', cursor:'pointer'}}>{isPlaying ? <PauseIcon style={iconSizeStyle} /> : <PlayIcon style={iconSizeStyle} />}</button><div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}><button onClick={() => handleVolumeChange({ target: { value: volume > 0 ? 0 : 1 } })} style={{background:'none', border:'none', color:'white', cursor:'pointer'}}>{volume > 0 ? <VolumeHighIcon style={iconSizeStyle} /> : <VolumeLowIcon style={iconSizeStyle} />}</button><input type="range" min="0" max="1" step="0.01" value={volume} onChange={handleVolumeChange} style={{width:'6rem'}} /></div><span style={{fontFamily:'monospace', fontSize:'0.875rem'}}>{formatTime(progress * duration)} / {formatTime(duration)}</span></div>
                        <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}><div style={{position:'relative'}} ref={speedControlRef}><button onClick={() => setShowSpeedOptions(p => !p)} style={{fontFamily:'monospace', fontSize:'0.875rem', width:'4rem', textAlign:'center', padding:'0.25rem 0.5rem', borderRadius:'0.25rem', background:'none', border:'none', color:'white', cursor:'pointer'}} title="Playback Speed">{playbackRate}x</button>{showSpeedOptions && (<div style={{position:'absolute', bottom:'100%', right:0, marginBottom:'0.5rem', backgroundColor:'rgba(0,0,0,0.7)', borderRadius:'0.5rem', padding:'0.25rem', zIndex:10}}>{[0.5, 1, 1.5, 2, 3].map(rate => (<button key={rate} onClick={() => handlePlaybackRateChange(rate)} style={{display:'block', width:'100%', textAlign:'center', fontFamily:'monospace', padding:'0.375rem 1rem', fontSize:'0.875rem', borderRadius:'0.375rem', background: playbackRate === rate ? '#34d399' : 'none', fontWeight: playbackRate === rate ? 'bold' : 'normal', border:'none', color:'white', cursor:'pointer'}}>{rate}x</button>))}</div>)}</div>{(<button onClick={() => setIsMaximized(!isMaximized)} title={isMaximized ? "Restore size" : "Maximize"} style={{background:'none', border:'none', color:'white', cursor:'pointer'}}>{isMaximized ? <MinimizeIcon style={iconSizeStyle} /> : <MaximizeIcon style={iconSizeStyle} />}</button>)}</div>
                    </div>
                 </div>
              )}
              <button onClick={handleClose} className="enhancer-modal-close-button">
                <CloseIcon style={closeIconStyle} />
              </button>
            </div>
          </div>
        </div>
      </div>,
      document.getElementById("enhancer-root")
    );
  };

  const AppManager = () => { /* ... (此组件的其余部分代码与上一版本完全相同，无需修改) ... */
    const [activeModalItem, setActiveModalItem] = useState(null);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const audioRef = useRef(null);
    const handleHotspotClick = useCallback((event) => {
        const hotspot = event.target.closest(".enhanced-hotspot");
        if (!hotspot) return;
        const { url, target, mediaType, iconType, popupWidth, popupHeight, description, aspectRatio } = hotspot.dataset;
        if (audioRef.current && !audioRef.current.paused) { audioRef.current.pause(); }
        if (mediaType === 'audio') {
            handleAudioPlay(hotspot, url);
        } else if (target === 'embed') {
            setActiveModalItem({ url, mediaType, description, popupWidth, popupHeight, aspectRatio, origin: { x: event.clientX, y: event.clientY } });
            setTimeout(() => setIsModalVisible(true), 10);
        } else {
             const width = popupWidth || 800; const height = popupHeight || 600;
             const features = target === 'popup' ? `width=${width},height=${height},resizable=yes,scrollbars=yes` : null;
             window.open(url, target === '_self' ? '_self' : '_blank', features);
        }
    }, []);
    const handleAudioPlay = (hotspot, url) => {
        const audio = audioRef.current;
        const isCurrentlyPlayingThis = hotspot.dataset.isPlaying === 'true';
        const anyPlaying = document.querySelector('[data-is-playing="true"]');
        if (anyPlaying && anyPlaying !== hotspot) { anyPlaying.removeAttribute('data-is-playing'); const ring = anyPlaying.querySelector('.audio-pulse-ring'); if(ring) ring.remove(); }
        if (isCurrentlyPlayingThis) {
            audio.pause();
        } else {
            audio.src = url;
            audio.play().catch(e => console.error("Audio play failed:", e));
            hotspot.dataset.isPlaying = 'true';
            const ring = document.createElement('div');
            ring.className = 'audio-pulse-ring';
            hotspot.appendChild(ring);
        }
    };
    const handleAudioPauseOrEnd = () => {
        const currentlyPlaying = document.querySelector('[data-is-playing="true"]');
        if (currentlyPlaying) {
            currentlyPlaying.removeAttribute('data-is-playing');
            const ring = currentlyPlaying.querySelector('.audio-pulse-ring');
            if(ring) ring.remove();
        }
    };
    const handleCloseModal = useCallback(() => { setIsModalVisible(false); setTimeout(() => setActiveModalItem(null), 500); }, []);
    useEffect(() => {
      document.body.addEventListener("click", handleHotspotClick);
      const audio = document.createElement('audio');
      audioRef.current = audio;
      audio.addEventListener('pause', handleAudioPauseOrEnd);
      audio.addEventListener('ended', handleAudioPauseOrEnd);
      document.body.appendChild(audio);
      return () => { document.body.removeEventListener("click", handleHotspotClick); audio.removeEventListener('pause', handleAudioPauseOrEnd); audio.removeEventListener('ended', handleAudioPauseOrEnd); if (document.body.contains(audio)) { document.body.removeChild(audio); } };
    }, [handleHotspotClick]);
    return ( <ModalPlayer item={activeModalItem} isVisible={isModalVisible} onClose={handleCloseModal} /> );
  };

  const rootElement = document.getElementById("enhancer-root");
  if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(<AppManager />);
  } else {
    console.error("Hotspot Enhancer Error: Root element '#enhancer-root' not found.");
  }

})();