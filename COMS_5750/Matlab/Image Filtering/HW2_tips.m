[X,MAP] = imread('StarWars.png');
imwrite(X,MAP,'StarWars.jpg','jpg');
a = imread('StarWars.jpg');
figure; imshow(a)

b = im2bw(a, 0.9);
figure; imshow(b)

bi = ~b;
figure; imshow(bi)

s = imread('A.png');
figure; imshow(s)
s1 = im2bw(s, 0.5);
se = ~s1;
figure; imshow(se)

Apos= imerode(bi, se);
figure; imshow(Apos)

OnlyAs = imdilate(Apos, se);
figure; imshow(OnlyAs)

