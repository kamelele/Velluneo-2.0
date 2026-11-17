#include <cmath>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <algorithm>
#include <vector>
using namespace std;
struct Case {double vac,hz,C,R,vd,L,P;};
int main(int argc,char**argv){
 double maxdt=stod(argv[1]);int waveid=argc>2?stoi(argv[2]):-1;
 ofstream wave;if(waveid>=0)wave.open(argv[3]);
 cout<<setprecision(15);if(wave)wave<<setprecision(15)<<"t,V,Ib,Ip,Ibleed,Ic\n";
 Case a;int id=0;
 while(cin>>a.vac>>a.hz>>a.C>>a.R>>a.vd>>a.L>>a.P){
 const double peak=.358522,Rbleed=499000*.979,T=1/(2*a.hz),end=20*T,start=16*T;
 const double fs=2*a.P/(a.L*peak*peak),Ts=1/fs;
 double V=a.vac*sqrt(2)-a.vd,t=0,cycle_start=0,ton=a.L*peak/V,next=ton;
 bool on=true;long grid=1;double vmin=1e9,vmax=0,imax=0;
 vector<double>s(12,0);double Estart=0;
 auto curr=[&](double tt,double vv){
  double ib=max(0.,(a.vac*sqrt(2)*abs(sin(2*M_PI*a.hz*tt))-a.vd-vv)/a.R);
  double ip=on?peak*max(0.,min(1.,(tt-cycle_start)/ton)):0.;
  double bleed=vv/Rbleed;return vector<double>{ib,ip,bleed,ib-ip-bleed};
 };
 while(t<end-1e-14){
  double boundary=min({next,grid*maxdt,end,start>t+1e-14?start:end});
  double h=boundary-t;if(h<1e-14){
   t=boundary;
  }else{
   auto a1=curr(t,V);double k1=a1[3]/a.C;
   auto a2=curr(t+h/2,V+h*k1/2);double k2=a2[3]/a.C;
   auto a3=curr(t+h/2,V+h*k2/2);double k3=a3[3]/a.C;
   auto a4=curr(t+h,V+h*k3);double k4=a4[3]/a.C;
   if(t>=start-1e-14){
    for(int q=0;q<4;q++){
     auto &i=q==0?a1:q==1?a2:q==2?a3:a4;double w=h*(q==0||q==3?1:2)/6;
     double vv=q==0?V:q==1?V+h*k1/2:q==2?V+h*k2/2:V+h*k3;
     s[0]+=w*i[0]*i[0];s[1]+=w*i[1]*i[1];s[2]+=w*i[2]*i[2];s[3]+=w*i[3]*i[3];s[4]+=w*i[0]*(i[1]+i[2]);s[5]+=w*(i[1]+i[2])*(i[1]+i[2]);s[6]+=w*vv*i[1];s[7]+=w*i[3];s[8]+=w*i[0];s[9]+=w*i[1];
     vmin=min(vmin,vv);vmax=max(vmax,vv);imax=max(imax,i[0]);
    }
   }
   V+=h*(k1+2*k2+2*k3+k4)/6;t=boundary;
  }
  if(abs(t-start)<1e-12)Estart=.5*a.C*V*V;
  bool atgrid=abs(t-grid*maxdt)<1e-12;
  if(abs(t-next)<1e-12){
   if(on){on=false;next=cycle_start+Ts;}
   else{cycle_start=next;on=true;ton=a.L*peak/V;next=cycle_start+ton;if(ton>=Ts) return 2;}
  }
  if(atgrid){
   if(id==waveid && t>=start){auto i=curr(t,V);wave<<t-start<<","<<V<<","<<i[0]<<","<<i[1]<<","<<i[2]<<","<<i[3]<<"\n";}
   grid++;
  }
 }
 double duration=end-start;for(double&x:s)x/=duration;
 double idres=s[3]-(s[0]+s[5]-2*s[4]);
 cout<<id<<","<<fs<<","<<vmin<<","<<vmax<<","<<sqrt(s[0])<<","<<sqrt(s[1])<<","<<sqrt(s[5])<<","<<sqrt(s[3])<<","<<s[4]<<","<<s[6]<<","<<s[7]<<","<<idres<<","<<imax<<","<<(.5*a.C*V*V-Estart)/duration<<"\n";
 id++;
 }
}
