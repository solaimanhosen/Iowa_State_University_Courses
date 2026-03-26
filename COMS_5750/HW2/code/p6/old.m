clear; clc; close all;

color_img = imread('./../../images/p6/in/1.jpg');
% color_img = imread('./../../images/p6/in/2.jpg');
figure; imshow(color_img); title('Original');

%% -- 1. Binarize (replicate im2bw 0.9) --------------------------------------
b  = im2bw(color_img, 0.5);         % white background -> 1, dark dots -> 0
bi = ~b;                    % invert: dots -> 1 (foreground)
figure; imshow(bi); title('Inverted binary');

%% -- 2. Read Structural Element

se = imread('./../../braille_cutouts/q.jpg');
se_bw = im2bw(se, 0.5);
q_strel = ~se_bw;

figure; imshow(q_strel); title('Q Structural Element');

se = imread('./../../braille_cutouts/w.jpg');
se_bw = im2bw(se, 0.5);
w_strel = ~se_bw;

figure; imshow(w_strel); title('W Structural Element');

se = imread('./../../braille_cutouts/y.jpg');
se_bw = im2bw(se, 0.5);
y_strel = ~se_bw;

figure; imshow(y_strel); title('Y Structural Element');

%% -- 3. Find Q positions
q_positions = imerode(bi, q_strel);
fprintf('Detected Q positions: %d\n', sum(q_positions(:)));

q_strel = imdilate(q_strel, strel('square', 3));

onlyQ = imdilate(q_positions, q_strel);
figure; imshow(onlyQ); title('Q character pixel mask');

% %% -- 4. Find W positions
w_positions = imerode(bi, w_strel);
fprintf('Detected W positions: %d\n', sum(w_positions(:)));

w_strel = imdilate(w_strel, strel('square', 3));

onlyW = imdilate(w_positions, w_strel);
figure; imshow(onlyW); title('W character pixel mask');

% %% -- 5. Find Y positions
y_positions = imerode(bi, y_strel);
fprintf('Detected Y positions: %d\n', sum(y_positions(:)));

y_strel = imdilate(y_strel, strel('square', 3));
onlyY = imdilate(y_positions, y_strel);
figure; imshow(onlyQ); title('Q character pixel mask');

%% -- 5. Color Q pixels GREEN in the original image --------------------------
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyQ == 1);
R(pos) = 255;
G(pos) = 255;
B(pos) = 255;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('Q characters colored WHITE');

% [X,MAP] = imread('./../../english_cutouts/q.png');
% imwrite(X,MAP,'q.jpg','jpg');
q_eng = imread('./../../english_cutouts/q.png');
q_eng_bw = im2bw(q_eng, 0.5);
q_eng_strel = ~q_eng_bw;
figure; imshow(q_eng_strel);

onlyQ = imdilate(q_positions, q_eng_strel);
figure; imshow(onlyW); title('W character pixel mask');

R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyQ == 1);
R(pos) = 0;
G(pos) = 0;
B(pos) = 0;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('W characters colored WHITE');

%% -- 6. Color W pixels GREEN in the original image --------------------------
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyW == 1);
R(pos) = 255;
G(pos) = 255;
B(pos) = 255;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('W characters colored WHITE');

w_eng = imread('./../../english_cutouts/w.jpg');
w_eng_bw = im2bw(w_eng, 0.5);
w_eng_strel = ~w_eng_bw;
figure; imshow(w_eng_strel);

onlyW = imdilate(w_positions, w_eng_strel);
figure; imshow(onlyW); title('W character pixel mask');

R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyW == 1);
R(pos) = 0;
G(pos) = 0;
B(pos) = 0;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('W characters colored WHITE');


%% -- 7. Color Y pixels GREEN in the original image --------------------------
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyY == 1);
R(pos) = 255;
G(pos) = 255;
B(pos) = 255;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('Y characters colored GREEN');


y_eng = imread('./../../english_cutouts/y.jpg');
y_eng_bw = im2bw(y_eng, 0.5);
y_eng_strel = ~y_eng_bw;
figure; imshow(y_eng_strel);

onlyY = imdilate(y_positions, y_eng_strel);
figure; imshow(onlyY); title('W character pixel mask');

R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyY == 1);
R(pos) = 0;
G(pos) = 0;
B(pos) = 0;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('W characters colored WHITE');

%% -- 8. Save result ---------------------------------------------------------
imwrite(color_img, './../../images/p6/out/1.jpg');
% imwrite(color_img, './../../images/p6/out/2.jpg');

