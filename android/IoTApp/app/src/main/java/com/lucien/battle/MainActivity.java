package com.lucien.battle;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONObject;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;

public class MainActivity extends AppCompatActivity {
    private EditText ip;
    private EditText port;
    private Button templum;
    private Button lumtemp;
    private Button send;
    private TextView tv;
    private TextView receive;
    private TextView connect;
    private Boolean tl = true;
    private Boolean lt = false;
    private Boolean start = false;
    private String sIp = null;
    private Integer iPort = null;

    public Button getTemplum() {
        return templum;
    }

    public void setTemplum(Button templum) {
        this.templum = templum;
    }

    public Button getLumtemp() {
        return lumtemp;
    }

    public void setLumtemp(Button lumtemp) {
        this.lumtemp = lumtemp;
    }

    public Button getSend() {
        return send;
    }

    public void setSend(Button send) {
        this.send = send;
    }

    public Boolean getTl() {
        return tl;
    }

    public void setTl(Boolean tl) {
        this.tl = tl;
    }

    public Boolean getLt() {
        return lt;
    }

    public void setLt(Boolean lt) {
        this.lt = lt;
    }

    public MainActivity getMa() {
        return ma;
    }

    public void setMa(MainActivity ma) {
        this.ma = ma;
    }

    private MainActivity ma = this;

    public EditText getIp() {
        return ip;
    }

    public void setIp(EditText ip) {
        this.ip = ip;
    }

    public EditText getPort() {
        return port;
    }

    public void setPort(EditText port) {
        this.port = port;
    }

    public TextView getTv() {
        return tv;
    }

    public void setTv(TextView tv) {
        this.tv = tv;
    }

    public TextView getReceive() {
        return receive;
    }

    public void setReceive(TextView receive) {
        this.receive = receive;
    }

    public TextView getConnect() {
        return connect;
    }

    public void setConnect(TextView connect) {
        this.connect = connect;
    }

    public Boolean getStart() {
        return start;
    }

    public void setStart(Boolean start) {
        this.start = start;
    }

    public String getsIp() {
        return sIp;
    }

    public void setsIp(String sIp) {
        this.sIp = sIp;
    }

    public Integer getiPort() {
        return iPort;
    }

    public void setiPort(Integer iPort) {
        this.iPort = iPort;
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /* Get reference to elements */
        this.ip = (EditText) findViewById(R.id.ip);
        this.port = (EditText) findViewById(R.id.port);

        this.templum = (Button) findViewById(R.id.templum);
        this.lumtemp = (Button) findViewById(R.id.lumtemp);
        this.send = (Button) findViewById(R.id.send);

        this.tv = (TextView) findViewById(R.id.tv);
        this.receive = (TextView) findViewById(R.id.receive);
        this.connect = (TextView) findViewById(R.id.connect);

        /* Initialize buttons */
        this.templum.setEnabled(!this.tl);
        this.lumtemp.setEnabled(!this.lt);

        /* Initialize listeners */
        /* When click on LT/TL buttons change wich button is ennable */
        this.templum.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                changeOrder();
            }
        });
        this.lumtemp.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                changeOrder();
            }
        });
        /* Send click event */
        this.send.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                /* Get IP */
                sIp = ip.getText().toString();

                /* Get Port and check if it's correct number */
                try {
                    iPort = Integer.parseInt(port.getText().toString());
                } catch (Exception e) {
                    iPort = null;
                }

                if (sIp != null) {
                    /* Default Port 10000 */
                    if (iPort == null) {
                        iPort = 10000;
                    }

                    /* Disable button until we receive the response */
                    send.setEnabled(false);

                    /* Send message LT/TL */
                    if (tl) {
                        sendData("TL\n");
                    }
                    if (lt) {
                        sendData("LT\n");
                    }

                } else {
                    /* If IP is null display error */
                    connect.setText("Connection impossible");
                }
            }
        });

    }

    /* Change the text of receive view */
    public void setTextViewResult(String result) {
        receive.setText(result);
    }

    /* Send message to server in UDP */
    private void sendData(String val) {
        if (!start) {
            /* Start receive */
            start = true;
            new Thread(new Runnable() {
                private DatagramSocket udpSocket;
                private DatagramPacket packet;
                private Boolean error = false;
                private String text;
                private JSONObject obj;

                public void run() {
                    try {
                        this.udpSocket = new DatagramSocket(iPort);
                    } catch (SocketException e) {
                        this.error = true;
                        Log.i("Error Dt", e.getMessage());
                    }
                    /* Always receive as long as no errors */
                    while (!this.error && start) {
                        try {

                            byte[] buffer = new byte[2048];
                            this.packet = new DatagramPacket(buffer, buffer.length);

                            Log.i("UDP client: ", "about to wait to receive");

                            this.udpSocket.receive(this.packet);

                            text = new String(buffer, 0, this.packet.getLength());

                            Log.i("Received data", text);
                            if (text.indexOf("retry") == -1) {
                                /* Convert text in JSON */
                                /*
                                * Exemple message format
                                * {"l": "0", "t": "28", "o": "LT"}
                                */
                                try {
                                    obj = null;
                                    obj = new JSONObject(text);

                                    Log.d("JSON", obj.toString());

                                } catch (Throwable tx) {
                                    obj = null;
                                    Log.e("JSON Error", "Could not parse malformed JSON: \"" + text + "\"");
                                }
                                runOnUiThread(new Runnable() {

                                    @Override
                                    public void run() {
                                        if (obj != null) {
                                            try {
                                                /* Change text of result view */
                                                /* In function of the order -> o parameter in JSON */
                                                String order = obj.getString("o");
                                                Log.d("Order", order);
                                                if (order.indexOf("TL") != -1) {
                                                    /* Temp the lum */
                                                    setTextViewResult("Temp :" + obj.getString("t") + "\nLum :" + obj.getString("l"));
                                                }
                                                if (order.indexOf("LT") != -1) {
                                                    /* Lum then temp */
                                                    setTextViewResult("Lum :" + obj.getString("l") + "\nTemp :" + obj.getString("t"));
                                                }
                                            } catch (Throwable tx) {
                                                setTextViewResult("Une erreur est survenue.");
                                            }
                                        } else {
                                            setTextViewResult("Une erreur est survenue.");
                                        }
                                        /* Set the send button enable because we receive a response */
                                        /* So user can send another message now */
                                        send.setEnabled(true);
                                    }
                                });
                            } else {
                                /* If text == retry */
                                /* Means an error happended */
                                /* Send again the message */
                                if (tl) {
                                    sendData("TL\n");
                                }
                                if (lt) {
                                    sendData("LT\n");
                                }
                            }
                        } catch (IOException e) {
                            Log.e("UDP", "error: ", e);
                            this.error = true;
                        }
                    }
                    start = false;
                    connect.setText("Connection impossible");
                }
            }).start();
        }
        /* Send message */
        new Send().execute(this.sIp, this.iPort, val, this);
    }

    /* When click on TL/LT button */
    private void changeOrder() {
        /* Change who is ennable */
        tl = !tl;
        lt = !lt;
        this.templum.setEnabled(!this.tl);
        this.lumtemp.setEnabled(!this.lt);

        /* Change the text */
        if(tl) {
            this.tv.setText("Temp - Lum");
        }
        if(lt) {
            this.tv.setText("Lum - Temp");
        }

    }
}
