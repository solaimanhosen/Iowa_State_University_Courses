

% a = imread('./../../images/p1/in/1.jpg');
a = imread('./../../images/p1/in/2.jpg');
figure; imshow(a)

b = im2bw(a, 0.9);
figure; imshow(b)

bi = ~b;
figure; imshow(bi)

s = imread('dot2.jpg');
figure; imshow(s)
s1 = im2bw(s, 0.5);
se = ~s1;
figure; imshow(se)

Apos= imerode(bi, se);
figure; imshow(Apos)

plus = [
    0 0 0 0 0 0 0 0 0 0 0;
    0 0 0 0 0 0 0 0 0 0 0;
    0 0 0 0 1 1 1 0 0 0 0; 
    0 0 0 0 1 1 1 0 0 0 0;
    0 0 1 1 1 1 1 1 1 1 0; 
    0 0 1 1 1 1 1 1 1 1 0; 
    0 0 1 1 1 1 1 1 1 1 0;
    0 0 0 0 1 1 1 0 0 0 0; 
    0 0 0 0 1 1 1 0 0 0 0; 
    0 0 0 0 1 1 1 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0;
    ];

onlyPlus = imdilate(Apos, plus);
figure; imshow(onlyPlus)

% change color of original image
color_img = a;

R = color_img(:, :, 1);
G = color_img(:, :, 2);
B = color_img(:, :, 3);

pos=find(onlyPlus==1);

R(pos) = 255;
G(pos) = 0;
B(pos) = 0;

color_img(:, :, 1) = R;
color_img(:, :, 2) = G;
color_img(:, :, 3) = B;

figure; imshow(color_img)

% Save result
% imwrite(color_img, './../../images/p1/out/1a.jpg');
imwrite(color_img, './../../images/p1/out/2a.jpg');
