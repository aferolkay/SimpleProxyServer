clear;
clc;
close all;

fprintf('Creating server socket...');
TCPIPServer = tcpserver('127.0.0.1', 6002); % w/proxy
%TCPIPServer = tcpserver('127.0.0.1', 6001); % just server
fprintf('SERVER CREATED\n');

global TABLE 
TABLE = [0, 0, 0 ,0, 0, 0, 0, 0, 0, 0];

while true
    if TCPIPServer.NumBytesAvailable ~= 0
        command = read(TCPIPServer, TCPIPServer.NumBytesAvailable, "string");
        reply(TCPIPServer,command)
    end
end    





function reply(srv, command)
    global TABLE;
    while (1) % try a few times, if you only try once you get an error saying client is not connected
        disp(command);
        %%%%%%      %%%%%%
        segmentedCommand = split(command,";");
        OP = split( segmentedCommand(1),"=");
        OP = OP(2);
        INDEX = split( segmentedCommand(2),"=");
        INDEX = INDEX(2);
        DATA = split( segmentedCommand(3),"=");
        DATA = DATA(2);
        %%%%%%      %%%%%%
        [retOP, retINDEX, retDATA] = applyCommand(OP, INDEX, DATA);
        REPLY = retOP+ retINDEX+ retDATA;
        try
            %disp(REPLY)
            srv.write(REPLY);
            break;
        catch
            pause(1); % wait for some amount
        end
    end
end



% 
function [retOP, retINDEX, retDATA] = applyCommand(OP, INDEX, DATA)
   global TABLE;
   retOP = "OP=";
   retINDEX="IND=";
   retDATA = "DATA=";
   indexes = split(INDEX,",");
   if length(indexes)> 9
      retINDEX = "invalid index!";
      return 
   end
   data = split(DATA,",");
   switch OP
   case "GET" 
      retOP = "OP=GET;";
      retINDEX = "IND="+INDEX+";";
      
      for i = 1:length(indexes)
        n = str2num(indexes(i))+1 ;
        m = TABLE(n);
        if i < length(indexes)
            retDATA =retDATA + num2str( TABLE(n) )+",";
        else
            retDATA =retDATA + num2str( TABLE(n) )+";";
        end
      end
       
   case "PUT"
       retOP = "OP=PUT;";
       retINDEX = "IND="+INDEX+";";
       retDATA = "DATA="+DATA+";";
       if isempty(indexes)
            return
       end
       for i = 1:length(indexes)
           n = str2num(indexes(i))+1 ;
           m = str2num(data(i));
           %disp(n)
           %disp(m)
           %disp(TABLE(n));
           TABLE(n) = m;
           %disp(TABLE(n));
       end
       disp(TABLE)
   case "CLR"
       retOP = "OP=CLR;";
       retINDEX = "IND="+";";
       retDATA = "DATA="+";";
       for i = 1:10
            TABLE(  i  ) = 0;
       end
       disp(TABLE)
   case "ADD"
       sum = 0 ;
       retOP = "OP=ADD;";
       retINDEX = "IND="+INDEX+";";
       
       for  i = 1:length(indexes)
            n = str2num(indexes(i)) +1;        
            sum = sum+TABLE( n ) ;
       end
       disp(sum);
       retDATA = "DATA="+num2str(sum)+";";
   otherwise
      disp("invalid OP");
   end

   return;
end