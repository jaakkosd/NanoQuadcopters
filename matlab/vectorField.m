clear

% resultX = zeros(17,17);
% resultY = zeros(17,17);

yi = 0;

for y = -3:0.2:3
    xi = 0;
    yi = yi + 1;
    for x = -3:0.2:3
        xi = xi + 1; 
        uVx = pfs(x,y);
        resultX(xi,yi) = uVx(1,1);
        resultY(xi,yi) = uVx(1,2);
    end
end

quiver(resultX.', resultY.');

function uvel = pfs(xC, yC)
R = 1; % Range when avoidance is activated
r = 0.5; % Safe distance
O = [0.01 0; 0.5 0.8];
xO = 0.01; % Obstacle x-coordinate
yO = 2; % Obstacle y-coordinate
constant = 0.25; % Constant to scale u values

uAx = 0; 
uAy = 0;

gx = 0;
gy = 4;
Kg = 0.05;

ugx = 0;
ugy = 0;


h = size(O,1);

isIn = 0;

for row = 1:h
    
    obstacle = O(row,:);

    dist = sqrt((obstacle(1) - xC)^2+(obstacle(2) - yC)^2); % Distance between agent and obstacle
    
    if dist < r
        isIn = 1;
    end

    if (r < dist && dist < R)
        uAxtemp = -(4*(R^2-r^2)*((dist)^2-R^2)*(xC-obstacle(1)))/(((dist)^2-r^2)^3);
        uAytemp = -(4*(R^2-r^2)*((dist)^2-R^2)*(yC-obstacle(2)))/(((dist)^2-r^2)^3);
        uAx = uAx + uAxtemp;
        uAy = uAy + uAytemp;
    end

end

if isIn == 0
    ugx = Kg*(2*gx - 2*xC);
    ugy = Kg*(2*gy - 2*yC);
end

u = [uAx, uAy];

if uAx ~= 0 || uAy ~= 0
    Ka = constant/sqrt(abs(uAx^2+uAy^2));
    u = Ka*u;
end

uAx = u(1);
uAy = u(2);

ux = ugx + uAx;
uy = ugy + uAy;

uvel = [ux, uy];
end