function process_video(input_path, output_path)
    vr = VideoReader(input_path);
    vr.CurrentTime = 0.0;
    mhist = uint8(zeros(vr.Height, vr.Width));

    vw = VideoWriter(output_path, 'MPEG-4');
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
        writeVideo(vw, mhist);
        mhist = mhist - 10;
        pFrameGray = cFrameGray;
    end

    close(vw);
    fprintf('  Saved: %s\n', output_path);
end

% --- Main ---
script_dir = fileparts(mfilename('fullpath'));
base_in    = fullfile(script_dir, '..', '..', 'images', 'p1', 'in');
base_out   = fullfile(script_dir, '..', '..', 'images', 'p1', 'out');

for vid_num = [1, 2]
    in_path  = fullfile(base_in,  sprintf('%d.mp4',  vid_num));
    out_path = fullfile(base_out, sprintf('%da.mp4', vid_num));
    fprintf('Processing video %d...\n', vid_num);
    process_video(in_path, out_path);
end

disp('Done.');
