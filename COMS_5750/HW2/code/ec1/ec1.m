clear; clc; close all;

% -------------------- CONFIG --------------------
imgPath    = fullfile('..','..','images','ec1','in','2.jpg');   % change to 2.jpg if needed
th         = 0.5;       % binarization threshold
dilateIter = 6;         % how many dilations to build grid mask
seSize     = 3;         % square strel size for dilation
margin     = 5;         % extra pixels added to r2/c2 crop (clamped safely)
debug      = false;     % set true to visualize intermediate crops/masks

brailleDir = fullfile('..','..','braille_cutouts');

% Order matters (to reduce false positives with erosion-only matching):
letters = ['y','z','w','x','v','u','q','p','r','l','t','s','n','m','o','k','g','d','f','h','j','b','c','e','i','a'];
% letters = ['v'];
% ------------------------------------------------

% --- Read image ---
a = imread(imgPath);
figure; imshow(a); title('Original');

% --- Binarize + invert (dots -> 1) ---
bi = binarizeInvert(a, th);
figure; imshow(bi); title('Inverted binary (dots=1)');

% --- Dilate several times to form blocks / help find grid gaps ---
se = strel('square', seSize);
d6 = bi;
for t = 1:dilateIter
    d6 = imdilate(d6, se);
end
figure; imshow(d6); title('Dilated mask');

% --- Find mid row indices of all-zero runs (grid lines / gaps) ---
rows = midIndicesOfZeroRuns(all(d6 == 0, 2));
cols = midIndicesOfZeroRuns(all(d6 == 0, 1));

rows = round(rows(:));
cols = round(cols(:));

% fprintf("rows: %d\n", numel(rows));
% fprintf("cols: %d\n", numel(cols));

% Optional: visualize grid lines
% output_img = a;
% for i = 1:numel(rows)
%     y = rows(i);
%     output_img = insertShape(output_img, 'Line', [1, y, size(output_img,2), y], ...
%         'Color', [255 0 0], 'LineWidth', 2);
% end
% for j = 1:numel(cols)
%     x = cols(j);
%     output_img = insertShape(output_img, 'Line', [x, 1, x, size(output_img,1)], ...
%         'Color', [255 0 0], 'LineWidth', 2);
% end
% figure; imshow(output_img); title('Grid lines');

% --- Crop each cell and print detected letters as a grid ---
output_img = a;
H = size(output_img, 1);
W = size(output_img, 2);

for i = 1:(numel(rows)-1)
    for j = 1:(numel(cols)-1)

        r1 = rows(i);
        r2 = rows(i+1) - 1 + margin;
        c1 = cols(j);
        c2 = cols(j+1) - 1 + margin;

        % Clamp to image bounds
        r1 = max(1, r1);  c1 = max(1, c1);
        r2 = min(H, r2);  c2 = min(W, c2);

        % Validate crop
        if r1 > r2 || c1 > c2
            fprintf(' '); % print blank
            continue;
        end

        patch = output_img(r1:r2, c1:c2, :);

        if debug
            figure; imshow(patch); title(sprintf('Patch r[%d:%d], c[%d:%d]', r1,r2,c1,c2));
        end
        % figure; imshow(patch); title(sprintf('Patch r[%d:%d], c[%d:%d]', r1,r2,c1,c2));

        letter = identifyLetter(patch, brailleDir, th, letters, debug);
        if letter == '\n'
            % fprintf("\n");
            break;
        else
            fprintf('%c', letter);
        end
    end
    fprintf('\n');  % new line after each row of cells
end

% ===================== FUNCTIONS =====================

function bi = binarizeInvert(color_img, thresh)
    % Compatible with your usage (im2bw supports RGB by converting to gray internally in many MATLAB versions)
    b  = im2bw(color_img, thresh);
    bi = ~b;  % dots -> 1
end

function strelMask = loadStrelFromImage(path, thresh)
    se = imread(path);
    strelMask = binarizeInvert(se, thresh);
end

function letter = identifyLetter(color_patch, brailleDir, thresh, letters, debug)
    % Returns a single character (e.g., 'q') or ' ' if nothing found.
    letter = ' ';

    bi = binarizeInvert(color_patch, thresh);

    if debug
        figure; imshow(bi); title('Patch binary (dots=1)');
    end

    for k = 1:numel(letters)
        ch = letters(k);
        braillePath = fullfile(brailleDir, [ch '.jpg']);

        if ~isfile(braillePath)
            continue;
        end

        strelMask = loadStrelFromImage(braillePath, thresh);

        positions = imerode(bi, strelMask);

        % figure; imshow(strelMask); title('strelMask');
        % figure; imshow(bi); title('Patch binary (dots=1)');
        % figure; imshow(positions);

        % if any(positions(:))
        %     letter = ch;
        %     return;
        % end
        % positions is a binary/logical image
        H = size(positions,1);
        W = size(positions,2);

        win = 20;                         % window size (10x10)
        r1 = floor((H - win)/2) + 1;
        c1 = floor((W - win)/2) + 1;
        r2 = min(H, r1 + win - 1);
        c2 = min(W, c1 + win - 1);

        centerPatch = positions(r1:r2, c1:c2);
        
        if any(centerPatch(:))
            letter = ch;
            return;
        end
    end
end

function mids = midIndicesOfZeroRuns(zeroVec)
    % zeroVec can be [H x 1] or [1 x W] logical
    zeroVec = logical(zeroVec);

    if iscolumn(zeroVec)
        d = diff([false; zeroVec; false]);
    else
        d = diff([false, zeroVec, false]);
    end

    starts = find(d == 1);
    ends_  = find(d == -1) - 1;

    mids = floor((starts + ends_) / 2);

    % Optional edge handling (same logic you had):
    if ~isempty(mids)
        if starts(1) == 1
            mids(1) = ends_(1);
        end
        if ends_(end) == numel(zeroVec)
            mids(end) = starts(end);
        end
    end
end
