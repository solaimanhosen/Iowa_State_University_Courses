% P1A
% vr = VideoReader('./../../images/p1/in/1.mp4');
vr = VideoReader('./../../images/p1/in/2.mp4');
vr.CurrentTime = 0.0;
mhist = uint8(zeros(vr.Height, vr.Width));

% --- Setup VideoWriter ---
% vw = VideoWriter('./../../images/p1/out/1a.mp4', 'MPEG-4');
vw = VideoWriter('./../../images/p1/out/2a.mp4', 'MPEG-4');
vw.FrameRate = vr.FrameRate;
open(vw);

if hasFrame(vr)
    pFrame = readFrame(vr);
    pFrameGray = im2gray(pFrame);
end

while hasFrame(vr)
    cFrame = readFrame(vr);
    cFrameGray = im2gray(cFrame);
    diff = uint8(abs(double(cFrameGray) - double(pFrameGray)));
    change = find(diff > 20);
    mhist(change) = 255;
    % imshow(mhist);
    
    % --- Write frame to video ---
    writeVideo(vw, mhist);
    
    mhist = mhist - 10;
    % pause(1/vr.FrameRate);
    pFrameGray = cFrameGray;
end

% --- Finalize video ---
close(vw);
disp('Motion history video saved.');