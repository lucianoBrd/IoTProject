package com.lucien.battle;

import android.os.AsyncTask;
import android.util.Log;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Send extends AsyncTask {
    private InetAddress address;
    private Boolean error = false;
    private String ip;
    private Integer port;
    private String val;
    private DatagramSocket s;
    private DatagramPacket p;
    private MainActivity ma;

    @Override
    protected Object doInBackground(Object[] objects) {
        this.ip = (String) objects[0];
        this.port = (Integer) objects[1];
        this.val = (String) objects[2];
        this.ma = (MainActivity) objects[3];
        Log.i("UDP client: ", "send " + this.val);
        /* Send val */
        try {
            this.address = InetAddress.getByName(this.ip);
            int msg_length = val.length();
            byte[] message = val.getBytes();

            this.s = new DatagramSocket();

            this.p = new DatagramPacket(message, msg_length, this.address, this.port);
            this.s.send(p);
            this.error = false;
        } catch (Exception ex) {
            Log.i("Error", ex.toString());
            this.error = true;
        }
        return this.error;
    }

    @Override
    protected void onPostExecute(Object result) {
        if (this.error) {
            ma.getConnect().setText("Connection impossible");
        } else {
            ma.getConnect().setText("Connecté");
        }
        ma.setStart(!this.error);
    }
}
