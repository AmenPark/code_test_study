import java.util.*;
class Node{
    int num;
    int costSum;
    HashSet<ArrayList<Integer>> edges;
    ArrayList<Integer> bestPath;
    public Node(int n){
        num=n;
        costSum=10000;
        edges=new HashSet<>();
    }
    
    public void back(ArrayList<Node> nodes){
        if (bestPath!=null){
            ArrayList<Integer> edge = new ArrayList<>();
            edge.add(bestPath.get(2));edge.add(-bestPath.get(1)); edge.add(bestPath.get(0));
            Node before=nodes.get(bestPath.get(0));
            before.edges.remove(bestPath);
            edges.add(edge);
            bestPath=null;
            before.back(nodes);
        }
    }
}
class Solution {
    int[][] chart;
    HashSet<Integer>[] conn1;
    HashSet<Integer>[] conn2;
    Queue<Integer> q;
    
    public int solution(int n1, int[][] g1, int n2, int[][] g2) {
        q = new LinkedList<>();
        chart= new int[n1+1][n2+1];
        conn1 = new HashSet[n1+1];
        conn2 = new HashSet[n2+1];
        for (int i=0;i<=n1;i++){
            conn1[i]=new HashSet<>();
        }
        for (int i=0;i<=n2;i++){
            conn2[i]=new HashSet<>();
        }
        for(int[] g:g1){
            conn1[g[0]].add(g[1]);
            conn1[g[1]].add(g[0]);
        }
        for(int[] g:g2){
            conn2[g[0]].add(g[1]);
            conn2[g[1]].add(g[0]);
        }
        
        ArrayList<Integer> toDo=new ArrayList<>();
        toDo.add(1);
        ArrayList<Integer> nextToDo=null;
        while(toDo.size()>0){
            nextToDo = new ArrayList<>();
            for(int i:toDo){
                for(int j:conn1[i]){
                    conn1[j].remove(i);
                    nextToDo.add(j);
                }
            }
            toDo=nextToDo;
        }
        toDo=new ArrayList<>();
        toDo.add(1);
        while(toDo.size()>0){
            nextToDo = new ArrayList<>();
            for(int i:toDo){
                for(int j:conn2[i]){
                    conn2[j].remove(i);
                    nextToDo.add(j);
                }
            }
            toDo=nextToDo;
        }
        return match(1,1);
    }
    public int match(int i, int j){
        if(chart[i][j]!=0){
            return chart[i][j];
        }
        if(conn1[i].size()==0||conn2[j].size()==0){
            chart[i][j]=1;
            return 1;
        }
        for(int x: conn1[i]){
            for (int y:conn2[j]){
                match(x,y);
            }
        }
        
        ArrayList<Node> nodes = new ArrayList<>();
        Node source = new Node(0);
        nodes.add(source);
        int n1 = conn1[i].size();
        int n2 = conn2[j].size();
        Node sink = new Node(n1+n2+1);
        ArrayList<Integer> edge = null;
        int x=0;
        int y=n1;
        for(int iValue:conn1[i]){
            x++;
            Node nd=new Node(x);
            nodes.add(nd);
            edge=new ArrayList<>();
            edge.add(0);edge.add(0);edge.add(x);
            source.edges.add(edge);
            y=n1;
            for (int jValue:conn2[j]){
                y++;
                edge=new ArrayList<>();
                edge.add(x);edge.add(-chart[iValue][jValue]);edge.add(y);
                nd.edges.add(edge);
            }
        }
        y=n1;
        for(int jValue:conn2[j]){
            y++;
            Node nd=new Node(y);
            nodes.add(nd);
            edge=new ArrayList<>();
            edge.add(y);edge.add(0);edge.add(n1+n2+1);
            nd.edges.add(edge);
        }
        nodes.add(sink);
        boolean[] inQ = new boolean[nodes.size()];
        int finalCost=1;
        while (spfa(nodes, inQ)){
            finalCost -= sink.costSum;
            sink.back(nodes);
        }
        chart[i][j]=finalCost;
        return finalCost;
    }
    public boolean spfa(ArrayList<Node> nodes, boolean[]inQ){
        clear(nodes);
        nodes.get(0).costSum=0;
        q.add(0);
        inQ[0]=true;
        int now, next_now;
        Node nowNd, next_nowNd;
        while(q.size()>0){
            now=q.poll();
            nowNd=nodes.get(now);
            for (ArrayList<Integer> edge:nowNd.edges){
                next_now=edge.get(2);
                next_nowNd=nodes.get(next_now);
                if(nowNd.costSum + edge.get(1) < next_nowNd.costSum){
                    next_nowNd.costSum=nowNd.costSum + edge.get(1);
                    next_nowNd.bestPath=edge;
                    if(!inQ[next_now]){
                        inQ[next_now]=true;
                        q.add(next_now);
                    }
                }
            }
            inQ[now]=false;
        }
        return (nodes.get(nodes.size()-1).costSum<0);
    }
    public void clear(ArrayList<Node> nodes){
        for(Node nd:nodes){
            nd.costSum=10000;
            nd.bestPath=null;
        }
    }
}
