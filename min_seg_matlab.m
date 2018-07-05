%interpolate segments that are too short
%probably doesn't work with Vase mode

cd 'C:\Users\Tom\Downloads';
filename = 'te2p-am-3.gcode';
filename_out = 'te2p-am-3-fixed.gcode';

l_min = 0.01; %minimum segment length 0.01 mm

fid = fopen(filename);
fo = fopen(filename_out, "w");

prevline = ';';
strset0 = ';';
newline = fgetl(fid);
plB = 0;
nlB = 0;
x0 = 0;
x1 = 0;
y0 = 0;
y1 = 0;

%cycle through all lines
while(newline)
  newline = fgetl(fid);
    if (~strcmp("G1", newline(1:2))) || (newline(4) == "E") || (newline(4) == "Z")
      
        %fputs(fo, strcat(prevline, "\n")); 
        fprintf(fo, strcat(prevline, "\n")); 
        prevline = newline;
        plB = 0;
    else
        nlB = 1;
        strset1 = strsplit(newline);
        x1 = str2num(strset1{2}(2:end));
        y1 = str2num(strset1{3}(2:end));
        if plB == 1
          distance = sqrt((x1-x0)^2 + (y1-y0)^2);
          if distance > l_min
            %if that distance was okay, write prevline to new file
            %prep for next cycle
            %fputs(fo, strcat(prevline, "\n")); 
            fprintf(fo, strcat(prevline, "\n"));
            prevline = newline;
            x0 = x1;
            y0 = y1;
            strset0 = strset1;
          %else
            %disp("modified");
            %prevline stays the same, newline is changed
          end
        else
          %fputs(fo, strcat(prevline, "\n")); 
          fprintf(fo, strcat(prevline, "\n")); 
          prevline = newline;
          plB = 1;
        end
    end
end

fclose(fo);
fclose(fid);  